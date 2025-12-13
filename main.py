"""FastAPI application for Multi-Agent Chat System."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from agents.coordinator import CoordinatorAgent
from memory.memory_manager import MemoryManager
from utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="Multi-Agent Chat System API",
    description="API for the Knowledge Representation and Reasoning multi-agent system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize coordinator and memory manager
memory_manager = MemoryManager()
coordinator = CoordinatorAgent(memory_manager=memory_manager, enable_llm=True)

class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    task_id: str
    user_query: str
    task_plan: Dict[str, Any]
    agent_results: List[Dict[str, Any]]
    final_answer: str
    memory_context_used: bool
    overall_confidence: float

class HealthResponse(BaseModel):
    status: str
    agents_available: List[str]
    llm_enabled: bool

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agents_available": [
            "CoordinatorAgent",
            "ResearchAgent",
            "AnalysisAgent",
            "MemoryAgent"
        ],
        "llm_enabled": coordinator.llm_client.is_available() if coordinator.llm_client else False
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a user query through the multi-agent system."""
    try:
        logger.info(f"Received query: {request.query}")
        
        result = coordinator.process_query(request.query, context=request.context)
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/memory/search")
async def search_memory(query: str, top_k: int = 5):
    """Search memory for relevant information."""
    try:
        results = coordinator.memory_agent.retrieve(query, search_type="hybrid", top_k=top_k)
        return results
    except Exception as e:
        logger.error(f"Error searching memory: {e}")
        raise HTTPException(status_code=500, detail=f"Error searching memory: {str(e)}")

@app.get("/memory/history")
async def get_conversation_history(limit: int = 10):
    """Get conversation history."""
    try:
        history = coordinator.memory_manager.get_conversation_history(limit=limit)
        return {"history": history}
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.delete("/memory/clear")
async def clear_memory():
    """Clear all memory (use with caution)."""
    try:
        coordinator.memory_manager.vector_store.clear()
        coordinator.memory_manager.conversation_history = []
        coordinator.memory_manager.knowledge_base = []
        coordinator.memory_manager.agent_state = {}
        return {"status": "Memory cleared"}
    except Exception as e:
        logger.error(f"Error clearing memory: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

