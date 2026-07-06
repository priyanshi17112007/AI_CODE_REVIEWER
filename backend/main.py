from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
import re
import ast
from dotenv import load_dotenv
import os

# Internal project schema and helper imports
from backend.schemas import QAReport, SecurityReport  
from  backend.agents import analyze_code_with_crew
from backend.validator import run_deterministic_syntax_check 
from crewai import Crew
from backend.database import SessionLocal, ReviewRecord
import openai
from backend.prompts import REVIEWGUARD_SYSTEM_PROMPT

# Load environment variables from .env file before anything else runs
load_dotenv()

app = FastAPI(title="Code Reviewer Engine")

# Configure Cross-Origin Resource Sharing (CORS) for frontend connection
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
    """Safely extracts and parses JSON content from markdown wrappers."""
    text = raw_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    
    return json.loads(text.strip())

def sanitize_source_code_input(code_content: str, filename: str) -> str:
    """
    PROMPT INJECTION SHIELD:
    Strips out docstrings and comments dynamically based on the file extension.
    This neutralizes any malicious 'SYSTEM OVERRIDE' commands before the LLM reads it.
    """
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == ".py":
        try:
            # Parse code into an Abstract Syntax Tree (AST) to securely remove docstrings
            tree = ast.parse(code_content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    if (node.body and 
                        isinstance(node.body[0], ast.Expr) and 
                        isinstance(node.body[0].value, ast.Constant) and 
                        isinstance(node.body[0].value.value, str)):
                        node.body.pop(0)
                        if not node.body:
                            node.body.append(ast.Pass())
            # Convert clean tree back to code string
            clean_code = ast.unparse(tree)
            # Regex fallback to remove remaining single-line comments (#)
            return re.sub(r"#.*?\n", "\n", clean_code)
        except Exception:
            # Fallback regex parsing if the file contains specific syntax variations
            return re.sub(r"#.*?\n", "\n", code_content)
            
    elif ext in [".java", ".c", ".cpp", ".js", ".ts"]:
        # Strip C-style multi-line (/* ... */) and single-line (// ...) comments
        pattern = r"(/\*([^*]|(\*+([^*/])))*\*+/)|(//.*)"
        return re.sub(pattern, "", code_content)
        
    return code_content


@app.post("/api/review")
async def review_code(submission: CodeSubmission, db: Session = Depends(get_db)):
    try:
        # ✅ FIX: request.code ki jagah hum submission.content nikal rahe hain
        code_content = submission.content
        file_name = submission.filename

        # -----------------------------------------------------------------
        # STEP 1: Local Deterministic Gatekeeper Check
        # -----------------------------------------------------------------
        issues = run_deterministic_syntax_check(code_content, file_name)

        if issues:

         vulnerabilities = []

         bugs = [
         {
            "bug_type": issue["type"],
            "line_number": issue["line"],
            "impact": "Compilation/Syntax Error",
            "description": issue["message"],
            "fix_suggestion": "Review your code syntax."
         }
         for issue in issues
         ]
   
         dynamic_score = 25

         record = ReviewRecord(
          filename=file_name,
          vulnerabilities=json.dumps(vulnerabilities),
          bugs=json.dumps(bugs),
          quality_score=dynamic_score,
          )

         db.add(record)
         db.commit()
         db.refresh(record)

         return {
          "id": record.id,
          "filename": record.filename,
          "quality_score": record.quality_score,
          "vulnerabilities": vulnerabilities,
          "bugs": bugs,
         }
        # -----------------------------------------------------------------
        # STEP 2: Trigger Shield & CrewAI Pipeline
        # -----------------------------------------------------------------
        hardened_code = sanitize_source_code_input(code_content, file_name)
        
        # CrewAI engine kickoff with standard parameters
        crew_output = await analyze_code_with_crew(hardened_code, file_name)
        
        tasks = crew_output.tasks_output
        raw_vulns = tasks[0].raw if len(tasks) > 0 else "[]"
        raw_bugs = tasks[1].raw if len(tasks) > 1 else "[]"

        # -----------------------------------------------------------------
        # STEP 3: Clean and Parse Payload Structures
        # -----------------------------------------------------------------
        try:
            parsed_vulns = clean_and_parse_json(raw_vulns)
            if isinstance(parsed_vulns, dict):
                vulnerabilities = parsed_vulns.get("vulnerabilities", [])
            else:
                vulnerabilities = parsed_vulns if isinstance(parsed_vulns, list) else []
        except Exception as e:
            vulnerabilities = [{
                "title": "Parsing Configuration Error", 
                "severity": "Medium", 
                "description": f"Failed to clean structural JSON: {str(e)}",
                "location": "Global Payload Parser",
                "remediation": "Review unescaped character blocks."
            }]

        try:
            parsed_bugs = clean_and_parse_json(raw_bugs)
            if isinstance(parsed_bugs, dict):
                bugs = parsed_bugs.get("bugs", [])
            else:
                bugs = parsed_bugs if isinstance(parsed_bugs, list) else []
        except Exception as e:
            bugs = [{
                "bug_type": "Data Pipeline Parsing Error", 
                "line_number": 0, 
                "impact": "Informational",
                "description": f"Failed to format system metrics output: {str(e)}", 
                "fix_suggestion": "// Check underlying evaluation syntax data strings."
            }]

        # -----------------------------------------------------------------
        # STEP 4: Production-Ready Calibrated Quality Score Engine
        # -----------------------------------------------------------------
        security_score = 100
        quality_score = 100
        is_syntactically_broken = False

        for v in vulnerabilities:
            if isinstance(v, dict):  
                severity = str(v.get("severity", "Low")).lower()
                if severity == "high": 
                    security_score -= 25 
                elif severity == "medium": 
                    security_score -= 15 
                else: 
                    security_score -= 5 

        for b in bugs:
            if isinstance(b, dict):  
                impact = str(b.get("impact", "Low")).lower()
                bug_type = str(b.get("bug_type", "")).lower()
                
                if "syntax" in bug_type or impact == "compilation error":
                    quality_score -= 40
                    is_syntactically_broken = True 
                elif impact == "high" or "runtime" in bug_type or "exception" in bug_type:
                    quality_score -= 20 
                elif "performance" in bug_type or "complexity" in bug_type:
                    quality_score -= 15 
                elif "informational" in impact or "warning" in bug_type or "style" in bug_type:
                    quality_score -= 5 
                else:
                    quality_score -= 10 

        security_score = max(0, security_score)
        quality_score = max(0, quality_score)

        if is_syntactically_broken:
            dynamic_score = 20
        else:
            dynamic_score = int((security_score * 0.5) + (quality_score * 0.5))
            dynamic_score = max(25, dynamic_score)

        # -----------------------------------------------------------------
        # STEP 5: Database Recording Routine
        # -----------------------------------------------------------------
        record = ReviewRecord(
            filename=file_name,
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
            "bugs": bugs
        }
        
    except Exception as e:
        print(f"❌ CRITICAL ENDPOINT ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_history(db: Session = Depends(get_db)):
    """Fetches full historical logging indices for user dashboard viewports."""
    records = db.query(ReviewRecord).order_by(ReviewRecord.id.desc()).all()
    return [{
        "id": r.id,
        "filename": r.filename,
        "quality_score": r.quality_score,
        "timestamp": r.timestamp
    } for r in records]