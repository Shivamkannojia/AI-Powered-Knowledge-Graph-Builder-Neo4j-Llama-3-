from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage

def get_llm():
    # Temperature 0 keeps it strict/factual
    return ChatOllama(model="llama3", temperature=0)

def get_graph_chain():
    """
    Fixes KeyError by treating the system prompt as raw text.
    """
    with open("generate_knowledge_graph.txt", "r") as f:
        system_text = f.read()
    
    # WE CHANGED THIS: Use SystemMessage to stop LangChain from parsing {}
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_text),
        ("human", "{content}")
    ])
    return prompt | get_llm() | StrOutputParser()

def get_router_chain():
    with open("router_model.txt", "r") as f:
        system_text = f.read()
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_text),
        ("human", "{input}")
    ])
    return prompt | get_llm() | StrOutputParser()

def get_qa_chain():
    with open("answer_question_model.txt", "r") as f:
        system_text = f.read()
        
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_text),
        ("human", "Context:\n{context}\n\nQuestion:\n{question}")
    ])
    return prompt | get_llm() | StrOutputParser()