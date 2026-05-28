import os
import re
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

def load_docs_from_blob(container_url: str) -> list[dict]:
    """Load all .md and .txt files from Azure Blob Storage docs container."""
    try:
        credential = ManagedIdentityCredential()
        client = BlobServiceClient(account_url=container_url, credential=credential)
    except Exception:
        credential = DefaultAzureCredential()
        client = BlobServiceClient(account_url=container_url, credential=credential)

    container_client = client.get_container_client("docs")
    docs = []

    for blob in container_client.list_blobs():
        if blob.name.endswith((".md", ".txt")):
            content = container_client.download_blob(blob.name).readall().decode("utf-8")
            docs.append({"name": blob.name, "content": content})

    return docs


def chunk_docs(docs: list[dict], chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """Split documents into overlapping chunks for better retrieval."""
    chunks = []

    for doc in docs:
        content = doc["content"]
        words = content.split()

        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            chunks.append({
                "source": doc["name"],
                "text": chunk_text,
                "index": len(chunks)
            })

    return chunks