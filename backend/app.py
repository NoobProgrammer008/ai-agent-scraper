import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ==================== IMPORTS ====================
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import asyncio
import csv
import os
from datetime import datetime
from typing import List

# Import ONLY what actually exists
from src.agents.research_agent import ResearchAgent

# Remove imports that don't exist:
# from src.utils.memory import Memory  ← DELETE THIS LINE
# from src.scrapers.web_scraper import WebScraper  ← DELETE IF NOT NEEDED

# ==================== SETUP ====================
app = FastAPI(title="Research Agent API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage
RESEARCH_HISTORY = []
RESULTS_DIR = "results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# ==================== DATA MODELS ====================
class ResearchRequest(BaseModel):
    query: str
    priority: str = "normal"

# ==================== ENDPOINTS ====================

@app.get("/")
def health_check():
    return {"status": "Research Agent API is online!"}

@app.get("/history")
def get_history(limit: int = 10):
    return {
        "count": len(RESEARCH_HISTORY),
        "history": RESEARCH_HISTORY[-limit:][::-1]
    }

@app.get("/results/{result_id}")
def get_result(result_id: int):
    for result in RESEARCH_HISTORY:
        if result["id"] == result_id:
            return result
    raise HTTPException(status_code=404, detail="Result not found")

@app.websocket("/ws/research")
async def websocket_research(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            message = await websocket.receive_text()
            request_data = json.loads(message)
            query = request_data.get("query")
            
            if not query:
                await websocket.send_json({
                    "status": "error",
                    "message": "Query is required"
                })
                continue
            
            await websocket.send_json({
                "status": "started",
                "message": f"Starting research on: {query}"
            })
            
            try:
                # Use your ResearchAgent
                agent = ResearchAgent()
                
                await websocket.send_json({
                    "status": "progress",
                    "message": "Searching the web..."
                })
                
                # Run agent
                results = agent.run(query)
                
                # Get memory from agent if it has it
                memory = agent.memory.get_summary() if hasattr(agent, 'memory') else {}
                
                await websocket.send_json({
                    "status": "progress",
                    "message": "Analyzing findings...",
                    "tool_calls": memory.get("tool_calls", 0) if memory else 0
                })
                
                await asyncio.sleep(0.5)
                
                # Save result
                result_id = len(RESEARCH_HISTORY) + 1
                result_entry = {
                    "id": result_id,
                    "query": query,
                    "timestamp": datetime.now().isoformat(),
                    "findings": str(results),
                    "memory": memory
                }
                RESEARCH_HISTORY.append(result_entry)
                
                await websocket.send_json({
                    "status": "completed",
                    "message": "Research complete!",
                    "results": results,
                    "memory": memory,
                    "result_id": result_id
                })
                
            except Exception as e:
                await websocket.send_json({
                    "status": "error",
                    "message": f"Research failed: {str(e)}"
                })
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    
    finally:
        await websocket.close()

@app.post("/export/{result_id}")
def export_result(result_id: int):
    result = None
    for r in RESEARCH_HISTORY:
        if r["id"] == result_id:
            result = r
            break
    
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    filename = f"{RESULTS_DIR}/research_{result_id}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Query", "Timestamp", "Findings"])
        writer.writerow([result["query"], result["timestamp"], result["findings"]])
    
    return FileResponse(
        filename,
        media_type="text/csv",
        filename=f"research_{result_id}.csv"
    )

@app.delete("/results/{result_id}")
def delete_result(result_id: int):
    global RESEARCH_HISTORY
    original_length = len(RESEARCH_HISTORY)
    RESEARCH_HISTORY = [r for r in RESEARCH_HISTORY if r["id"] != result_id]
    
    if len(RESEARCH_HISTORY) == original_length:
        raise HTTPException(status_code=404, detail="Result not found")
    
    filename = f"{RESULTS_DIR}/research_{result_id}.csv"
    if os.path.exists(filename):
        os.remove(filename)
    
    return {"success": True, "message": f"Result {result_id} deleted"}

# ==================== RUN ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)



