from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from pathlib import Path
import json
from ai import ask_ai
from connectors import fetch_by_platform


app = FastAPI()


memory = []


class ChatRequest(BaseModel):
    message: str


class ExplainRequest(BaseModel):
    product_name: str


# Enable CORS so the frontend (served from filesystem or other origin) can call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve the frontend static files from the sibling `frontend` directory
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")


@app.get("/")
def root():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Frontend not found"}


@app.get("/api/health")
def health():
    return {"message": "AI Product Chatbot Running"}




@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        reply = ask_ai(request.message, memory)

        memory.append({
            "role": "user",
            "content": request.message
        })

        # if reply is structured (dict), store its JSON string in memory for context
        if isinstance(reply, dict):
            memory.append({
                "role": "assistant",
                "content": json.dumps(reply)
            })
            return {"reply": reply}

        memory.append({
            "role": "assistant",
            "content": reply
        })

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post("/api/explain")
def explain(request: ExplainRequest):
    try:
        prompt = (
            f"You are an AI product recommendation assistant. Explain why the product '{request.product_name}' "
            "is a strong recommendation. Include pros, cons, and when it is the best choice."
        )
        reply = ask_ai(prompt, memory)

        memory.append({
            "role": "user",
            "content": f"Why this? {request.product_name}"
        })

        if isinstance(reply, dict):
            memory.append({"role": "assistant", "content": json.dumps(reply)})
            return {"reply": reply}

        memory.append({"role": "assistant", "content": reply})
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")



class FetchRequest(BaseModel):
    platform: str
    query: str


@app.post("/api/fetch_products")
def fetch_products(req: FetchRequest):
    # Fetch products from a named platform; connectors return mock data when no API keys
    items = fetch_by_platform(req.platform, req.query)
    return {"items": items}