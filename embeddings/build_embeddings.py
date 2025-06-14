import json
import nltk
import openai
import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

nltk.download('punkt')

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="../embeddings/"))
collection = client.get_or_create_collection("tds")

def chunk_text(text, size=500):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) < size:
            chunk += sentence + " "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + " "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

with open("../data/discourse_posts.json") as f:
    data = json.load(f)

for i, post in enumerate(data):
    text = post["content"]
    chunks = chunk_text(text)
    for chunk in chunks:
        embedding = openai.Embedding.create(
            input=chunk,
            model="text-embedding-ada-002"
        )["data"][0]["embedding"]
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{i}-{hash(chunk)}"]
        )

client.persist()
