from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
from typing import Optional

from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from tasks import help_patients, nutrition_analysis, exercise_planning, verification

app = FastAPI(
    title="Blood Test Report Analyzer",
    description="API for analyzing blood test reports and providing health recommendations",
    version="1.0.0"
)

def run_crew(query: str, file_path: str):
    """Run the crew with all agents to analyze the blood report"""
    medical_crew = Crew(
        agents=[doctor, verifier, nutritionist, exercise_specialist],
        tasks=[
            help_patients,
            nutrition_analysis,
            exercise_planning,
            verification
        ],
        process=Process.sequential,
        verbose=2
    )
    
    result = medical_crew.kickoff(inputs={'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Blood Test Report Analyzer API is operational"
    }

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: Optional[str] = Form("Summarize my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )

    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        response = run_crew(
            query=query.strip(),
            file_path=file_path
        )
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing blood report: {str(e)}"
        )
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
