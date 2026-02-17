# AI Knowledge Graph Builder

This project is a local tool that converts unstructured text into a structured Knowledge Graph using **Neo4j** and **Llama 3** (via Ollama). It allows you to build a graph from scratch by typing sentences and then chat with that data using a simple RAG (Retrieval-Augmented Generation) pipeline.

## Tech Stack
* **Database:** Neo4j (Graph Database)
* **LLM:** Llama 3 (running locally via Ollama)
* **Framework:** LangChain
* **Frontend:** Streamlit
* **Visualization:** Pyvis

## Features
* **Text-to-Graph:** Takes raw text (e.g., "Elon Musk is the CEO of Tesla") and automatically generates Cypher queries to insert nodes and relationships.
* **Smart Routing:** An AI router decides if your input is adding new data or asking a question about existing data.
* **Interactive Visualization:** Real-time visual rendering of the graph network using Pyvis.
* **Contextual QA:** Answers questions based strictly on the relationships found in the graph.

## Setup & Run

1.  **Prerequisites**
    * Install [Neo4j Desktop](https://neo4j.com/download/) and start a local database.
    * Install [Ollama](https://ollama.com/) and pull the model: `ollama pull llama3`.

2.  **Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    NEO4J_URI=neo4j://127.0.0.1:7687
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=your_password
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```
