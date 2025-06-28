from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import os
import uuid
from celery.result import AsyncResult
from database import get_db, AnalysisResult
from celery_worker import analyze_report_task
from sqlalchemy.orm import Session
import json

app = FastAPI(
    title="Blood Test Report Analyzer",
    description="API for analyzing blood test reports with queue and database",
    version="2.0.0"
)

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: Optional[str] = Form("Summarize my Blood Test Report"),
    user_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, "Only PDF files are accepted")

    file_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        task = analyze_report_task.delay(file_path, query, user_id)
        return JSONResponse({"task_id": task.id})
        
    except Exception as e:
        raise HTTPException(500, f"Error processing request: {str(e)}")

@app.get("/results/{task_id}")
async def get_result(task_id: str, db: Session = Depends(get_db)):
    task_result = AsyncResult(task_id)
    
    if not task_result.ready():
        return JSONResponse({"status": "processing"})
    
    result = task_result.get()
    
    if result["status"] == "success":
        db_result = db.query(AnalysisResult).filter(
            AnalysisResult.id == result["result_id"]
        ).first()
        
        return {
            "status": "complete",
            "result": json.loads(db_result.analysis),
            "metadata": {
                "file_name": db_result.file_name,
                "query": db_result.query,
                "created_at": db_result.created_at.isoformat()
            }
        }
    else:
        return JSONResponse(result, status_code=500)

@app.get("/history")
async def get_history(
    user_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    results = db.query(AnalysisResult).filter(
        AnalysisResult.user_id == user_id
    ).order_by(
        AnalysisResult.created_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": r.id,
            "file_name": r.file_name,
            "query": r.query,
            "created_at": r.created_at.isoformat()
        }
        for r in results
    ]
