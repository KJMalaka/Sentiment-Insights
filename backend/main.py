from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv
import json

load_dotenv()

from adapters import get_adapter
from services.sentiment import analyze_comments
from services.insights import compute_insights
from database import engine, get_db, init_db
from models.video import VideoAnalysis

# Initialize DB
init_db()

app = FastAPI(title="Social Sentiment & Brand Ambassador Fit Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str

@app.post("/api/analyze")
def analyze_video(req: AnalyzeRequest, db: Session = Depends(get_db)):
    url = req.url
    
    # 1. Platform Detection
    try:
        adapter = get_adapter(url)
        video_id = adapter.extract_video_id(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # 2. Check Cache
    cached = db.query(VideoAnalysis).filter(VideoAnalysis.video_id == video_id).first()
    if cached:
        return json.loads(cached.analysis_json)
        
    # 3. Fetch Data
    video_data = adapter.fetch_video_data(video_id)
    comments = video_data.get("comments", [])
    
    if not comments:
        raise HTTPException(status_code=400, detail="No comments found or comments are disabled.")
        
    # 4. Analyze Comments
    analyzed_comments = analyze_comments(comments)
    
    # 5. Compute Insights & Ambassador Score
    insights = compute_insights(video_data, analyzed_comments)
    platform = adapter.__class__.__name__.replace("Adapter", "").lower()

    response_data = {
        "video_data": video_data,
        "comments": analyzed_comments,
        "insights": insights,
        "platform": platform
    }

    # 6. Cache Result
    new_analysis = VideoAnalysis(
        video_id=video_id,
        platform=platform,
        analysis_json=json.dumps(response_data)
    )
    db.add(new_analysis)
    db.commit()
    
    return response_data
