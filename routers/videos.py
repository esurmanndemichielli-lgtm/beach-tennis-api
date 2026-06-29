from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import VideoJob
import uuid
import os
from services.ai_pipeline import process_video

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

jobs = {}

@router.post("/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed = ["video/mp4", "video/quicktime", "video/avi"]
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Formato invalido.")

    job_id = str(uuid.uuid4())
    filename = job_id + "_" + file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    db_job = VideoJob(
        job_id=job_id,
        filename=filename,
        filepath=filepath,
        status="queued",
        progress=0.0,
        current_step="Na fila de processamento",
    )
    db.add(db_job)
    db.commit()

    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0.0,
        "current_step": "Na fila de processamento",
        "steps_completed": [],
        "filename": filename,
        "stats": None,
        "error": None,
    }

    background_tasks.add_task(process_video_and_save, filepath, job_id, jobs, db)

    return {"job_id": job_id, "message": "Video recebido!", "filename": file.filename}

def process_video_and_save(filepath: str, job_id: str, jobs: dict, db: Session):
    from database import SessionLocal
    import json
    db2 = SessionLocal()
    try:
        result = process_video(filepath, job_id, jobs)
        db_job = db2.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if db_job and result:
            db_job.status = "completed"
            db_job.progress = 1.0
            db_job.current_step = "Concluido"
            db_job.stats_json = json.dumps(result)
            db2.commit()
    except Exception as e:
        print("Erro ao salvar no banco:", e)
    finally:
        db2.close()

@router.get("/status/{job_id}")
async def get_status(job_id: str, db: Session = Depends(get_db)):
    if job_id in jobs:
        return jobs[job_id]
    db_job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job nao encontrado.")
    import json
    stats = json.loads(db_job.stats_json) if db_job.stats_json else None
    return {
        "job_id": db_job.job_id,
        "status": db_job.status,
        "progress": db_job.progress,
        "current_step": db_job.current_step,
        "steps_completed": [],
        "stats": stats,
        "error": db_job.error,
    }

@router.get("/jobs")
async def list_jobs(db: Session = Depends(get_db)):
    db_jobs = db.query(VideoJob).order_by(VideoJob.created_at.desc()).all()
    return [{"job_id": j.job_id, "filename": j.filename, "status": j.status, "progress": j.progress} for j in db_jobs]
