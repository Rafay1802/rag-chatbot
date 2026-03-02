import os
from pinecone import Pinecone
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

def query_rag(question: str, namespace: str = "default") -> str:
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

    # Search Pinecone for relevant chunks
    results = index.search(
        namespace=namespace,
        query={
            "top_k": 5,
            "inputs": {"text": question}
        },
        fields=["text", "chunk_text", "content", "_node_content"]
    )

    # Extract text from results - try multiple field names
    context = ""
    hits = results.get("result", {}).get("hits", [])
    
    print(f"Found {len(hits)} hits")  # debug
    
    for hit in hits:
        fields = hit.get("fields", {})
        print(f"Fields available: {fields.keys()}")  # debug
        text = (
            fields.get("text") or
            fields.get("chunk_text") or
            fields.get("content") or
            fields.get("_node_content") or
            ""
        )
        context += text + "\n\n"

    print(f"Context length: {len(context)}")  # debug

    if not context.strip():
        return "Could not retrieve context from the database. Try reloading the URL."

    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile"
    )

    messages = [
        SystemMessage(content=f"""You are a helpful assistant. 
Answer the user's question based ONLY on the context below.
If the answer isn't in the context, say "I don't have enough information to answer that."

Context:
{context}"""),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)
    return response.content