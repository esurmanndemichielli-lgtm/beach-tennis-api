from pydantic import BaseModel
from typing import Optional

class VideoUpload(BaseModel):
    filename: str
    size_bytes: int
    duration_seconds: Optional[int] = None

class ProcessingStatus(BaseModel):
    job_id: str
    status: str
    progress: float
    current_step: str
    steps_completed: list
    estimated_seconds_remaining: Optional[int] = None
    error: Optional[str] = None
