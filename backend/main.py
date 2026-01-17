from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Ensure modules are in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.fusion import FusionEngine

app = FastAPI(title="Sentinel Intelligence API", version="4.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Engine Instance (Loads models once)
print("Initializing Fusion Engine (Heavy Models)...")
engine = FusionEngine()
print("Fusion Engine Ready.")

class PredictionRequest(BaseModel):
    ticker: str
    name: str

@app.get("/")
def health_check():
    return {"status": "active", "system": "Sentinel Cortex v4.0"}

@app.post("/predict")
def predict_stock(request: PredictionRequest):
    try:
        print(f"Analyzing {request.ticker} ({request.name})...")
        result = engine.run_analysis(request.ticker)
        
        if not result:
            raise HTTPException(status_code=404, detail="Analysis failed or returned no data")
            
        # Enrich result with request metadata if needed
        result["ticker"] = request.ticker
        result["name"] = request.name
        
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Clean output for professional look
    uvicorn.run(app, host="127.0.0.1", port=8000)
