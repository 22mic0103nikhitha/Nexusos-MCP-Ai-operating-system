from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Import the new agent process_query function
from agents.agent import process_query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI client to point to local Ollama
client = OpenAI(
    base_url=os.getenv("OLLAMA_URL", "http://localhost:11434/v1"),
    api_key='ollama' # Required by SDK but unused by Ollama
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "NexusOS Backend Running"}

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        # Route directly to the autonomous agent
        response_text = await process_query(req.message)
        
        return {"response": response_text}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
