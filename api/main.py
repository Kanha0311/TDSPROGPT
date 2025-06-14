from fastapi import FastAPI, Request
from api.rag_pipeline import retrieve_context, ask_gpt

app = FastAPI()

@app.post("/api/")
async def get_answer(request: Request):
    data = await request.json()
    question = data.get("question", "")

    context = retrieve_context(question)
    answer = ask_gpt(question, context)

    return {"answer": answer}
