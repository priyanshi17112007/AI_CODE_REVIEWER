from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file before anything else runs
load_dotenv()

from database import SessionLocal, ReviewRecord
from agents import analyze_code_with_crew

app = FastAPI(title=" Code Reviewer Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSubmission(BaseModel):
    filename: str
    content: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clean_and_parse_json(raw_text: str):
    text = raw_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    
    return json.loads(text.strip())

@app.post("/api/review")
async def review_code(submission: CodeSubmission, db: Session = Depends(get_db)):
    try:
        # Trigger CrewAI processing pipeline
        
        crew_output = await analyze_code_with_crew(submission.content)
        
        # 2. Extract specific raw outputs from individual tasks safely
        tasks = crew_output.tasks_output
        raw_vulns = tasks[0].raw if len(tasks) > 0 else "[]"
        raw_bugs = tasks[1].raw if len(tasks) > 1 else "[]"

        # 3. Clean and parse text into true Python list dictionaries
        try:
            vulnerabilities = clean_and_parse_json(raw_vulns)
        except Exception as e:
            print(f"⚠️ Security Parse Warning: {e}. Falling back to raw container.")
            vulnerabilities = [{"severity": "Medium", "title": "Parsing Error", "location": "System", "description": "Could not structure data cleanly."}]

        try:
            bugs = clean_and_parse_json(raw_bugs)
        except Exception as e:
            print(f"⚠️ QA Parse Warning: {e}. Falling back to raw container.")
            bugs = [{"bug_type": "Parsing Error", "impact": "Medium", "fix_suggestion": "Review raw agent logs."}]

        # 4. Generate a Live, Dynamic Quality Score based on findings
        # Start at 100 and deduct points dynamically for each issue caught
        dynamic_score = 100
        for v in vulnerabilities:
            severity = v.get("severity", "Low").lower()
            if severity == "high": dynamic_score -= 15
            elif severity == "medium": dynamic_score -= 10
            else: dynamic_score -= 5

        for b in bugs:
            impact = b.get("impact", "Low").lower()
            if "high" in impact or "exponential" in impact: dynamic_score -= 10
            else: dynamic_score -= 5

        # Ensure the score stays within reasonable boundaries (0 - 100)
        dynamic_score = max(0, min(100, dynamic_score))
        record = ReviewRecord(
            filename=submission.filename,
            vulnerabilities=json.dumps(vulnerabilities),
            bugs=json.dumps(bugs),
            quality_score=dynamic_score
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "id": record.id,
            "filename": record.filename,
            "quality_score": record.quality_score,
            "vulnerabilities": vulnerabilities,
            "bugs":bugs
        }
    except Exception as e:
        print(f"❌ CRITICAL ENDPOINT ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history(db: Session = Depends(get_db)):
    records = db.query(ReviewRecord).order_by(ReviewRecord.id.desc()).all()
    return [{
        "id": r.id,
        "filename": r.filename,
        "quality_score": r.quality_score,
        "timestamp": r.timestamp
    } for r in records]