import openai
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = chromadb.PersistentClient(path="../embeddings/")
collection = client.get_or_create_collection("tds")
def retrieve_context(question, k=3):
    question_embedding = openai.Embedding.create(
        input=question,
        model="text-embedding-ada-002"
    )["data"][0]["embedding"]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=k
    )

    documents = results['documents'][0]
    return "\n".join(documents)

def ask_gpt(question, context):
    prompt = f"Use the following course context to answer:\n\n{context}\n\nQuestion: {question}\nAnswer:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful teaching assistant for IIT Madras TDS course."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

