import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

def store_embeddings(chunks: list[str], namespace: str = "default"):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

    records = []
    for i, chunk in enumerate(chunks):
        records.append({
            "id": f"{namespace}-chunk-{i}",
            "text": chunk
        })

    # Upsert in batches of 50
    batch_size = 50
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        index.upsert_records(namespace=namespace, records=batch)
        print(f"Stored batch {i//batch_size + 1}")

    print(f"✅ Total stored: {len(records)} chunks")