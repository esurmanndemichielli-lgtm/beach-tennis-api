from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

jobs = {}

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    allowed = ["video/mp4", "video/quicktime", "video/avi"]
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Formato invalido.")

    job_id = str(uuid.uuid4())
    filename = job_id + "_" + file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0.0,
        "current_step": "Na fila de processamento",
        "steps_completed": [],
        "estimated_seconds_remaining": 120,
        "filename": filename,
        "stats": None,
        "error": None,
    }

    return {"job_id": job_id, "message": "Video recebido!", "filename": file.filename}

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job nao encontrado.")
    return jobs[job_id]

@router.get("/jobs")
async def list_jobs():
    return list(jobs.values())
