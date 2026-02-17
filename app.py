import streamlit as st
from llm_engine import get_graph_chain, get_router_chain, get_qa_chain
from database import Neo4jConnection
import os
from dotenv import load_dotenv
from pyvis.network import Network
import streamlit.components.v1 as components

load_dotenv()

# --- HELPER: Clean Cypher ---
def extract_cypher(text):
    text = text.replace("```cypher", "").replace("```", "").replace("\n", " ")
    raw_queries = text.split(";")
    valid_queries = []
    for q in raw_queries:
        q = q.strip()
        if q.upper().startswith(("CREATE", "MERGE", "MATCH")):
            valid_queries.append(q)
    return valid_queries

# --- HELPER: Visualizer ---
def visualize_graph(db_connection):
    # 1. Fetch all nodes and relationships
    query = "MATCH (n)-[r]->(m) RETURN n.name AS source, type(r) AS edge, m.name AS target LIMIT 50"
    data = db_connection.query(query)
    
    if not data:
        return None

    # 2. Create Pyvis Network
    net = Network(height="500px", width="100%", directed=True)    
    for record in data:
        src = record['source']
        tgt = record['target']
        edge = record['edge']
        
        # Add nodes and edge
        net.add_node(src, label=src, color="#4caf50", title=src) # Green bubbles
        net.add_node(tgt, label=tgt, color="#2196f3", title=tgt) # Blue bubbles
        net.add_edge(src, tgt, title=edge, label=edge)

    # 3. Save and return HTML
    path = "graph_viz.html"
    net.save_graph(path)
    return path

# --- SETUP ---
st.set_page_config(layout="wide", page_title="Neo4j Knowledge Graph")
st.title("AI Knowledge Graph Builder")

# Connect to DB
try:
    URI = os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687")
    USER = os.getenv("NEO4J_USERNAME", "neo4j")
    PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    if 'db' not in st.session_state:
        st.session_state.db = Neo4jConnection(URI, USER, PASSWORD)
    st.sidebar.success("✅ Database Connected")
except Exception as e:
    st.sidebar.error(f"❌ Connection Error: {e}")
    st.stop()

# --- TABS ---
tab1, tab2 = st.tabs(["💬 Chat / Generator", "🕸️ Graph Visualization"])

with tab1:
    user_input = st.text_area("Enter Text or Question:", height=100)
    
    if st.button("Run AI"):
        if not user_input:
            st.warning("Please type something.")
        else:
            # 1. ROUTER
            with st.spinner("Routing..."):
                router = get_router_chain()
                decision = router.invoke({"input": user_input}).lower().strip()
                if "generate" in decision: decision = "generate"
                elif "answer" in decision: decision = "answer"
                st.info(f"🤖 AI Intent: {decision.upper()}")

            # 2. GENERATE
            if decision == "generate":
                with st.spinner("Generating Graph Data..."):
                    chain = get_graph_chain()
                    raw_response = chain.invoke({"content": user_input})
                    queries = extract_cypher(raw_response)
                    
                    if not queries:
                        st.warning("No valid queries found.")
                    
                    try:
                        count = 0
                        for q in queries:
                            st.session_state.db.query(q)
                            count += 1
                        if count > 0:
                            st.success(f"✅ Executed {count} queries!")
                        else:
                            st.error("Failed to generate valid Cypher.")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

            # 3. ANSWER
            elif decision == "answer":
                with st.spinner("Searching..."):
                    context_query = "MATCH (n)-[r]->(m) RETURN n.name, type(r), m.name LIMIT 50"
                    context_data = st.session_state.db.query(context_query)
                    
                    qa_chain = get_qa_chain()
                    answer = qa_chain.invoke({
                        "context": str(context_data),
                        "question": user_input
                    })
                    st.markdown(f"### 💡 Answer: \n{answer}")

with tab2:
    st.subheader("Interactive Graph View")
    if st.button("Refresh Graph"):
        html_path = visualize_graph(st.session_state.db)
        if html_path:
            with open(html_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            components.html(source_code, height=500)
        else:
            st.warning("Graph is empty. Go to 'Chat' and generate some data first!")