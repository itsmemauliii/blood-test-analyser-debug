from celery import Celery
from main import run_crew
from database import AnalysisResult, SessionLocal
import os

celery = Celery(
    'tasks',
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

@celery.task
def analyze_report_task(file_path: str, query: str, user_id: str = None):
    try:
        analysis = run_crew(query=query, file_path=file_path)
        
        db = SessionLocal()
        db_result = AnalysisResult(
            file_name=file_path.split("/")[-1],
            query=query,
            analysis=str(analysis),
            user_id=user_id
        )
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        db.close()
        
        return {
            "status": "success",
            "result_id": db_result.id,
            "analysis": str(analysis)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
