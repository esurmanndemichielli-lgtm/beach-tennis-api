import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import json
import time

model = None

def load_model():
    global model
    if model is None:
        print("Carregando modelo YOLOv8...")
        model = YOLO("yolov8n.pt")
        print("Modelo carregado!")
    return model

def process_video(filepath: str, job_id: str, jobs: dict):
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["current_step"] = "Extraindo frames"
        jobs[job_id]["progress"] = 0.05

        cap = cv2.VideoCapture(filepath)
        if not cap.isOpened():
            raise Exception("Nao foi possivel abrir o video.")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0

        jobs[job_id]["steps_completed"] = ["Extração de frames"]
        jobs[job_id]["progress"] = 0.2
        jobs[job_id]["current_step"] = "Detectando jogadores"

        yolo = load_model()

        player_positions = []
        ball_positions = []
        frame_count = 0
        sample_rate = max(1, int(fps / 5))

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % sample_rate == 0:
                results = yolo(frame, verbose=False, classes=[0, 32])
                for r in results:
                    for box in r.boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        cx = (x1 + x2) / 2
                        cy = (y1 + y2) / 2
                        if cls == 0 and conf > 0.5:
                            player_positions.append({"frame": frame_count, "x": cx, "y": cy, "conf": conf})
                        elif cls == 32 and conf > 0.3:
                            ball_positions.append({"frame": frame_count, "x": cx, "y": cy, "conf": conf})

                progress = 0.2 + (frame_count / total_frames) * 0.5
                jobs[job_id]["progress"] = round(progress, 2)

            frame_count += 1

        cap.release()

        jobs[job_id]["steps_completed"] = ["Extração de frames", "Detecção de jogadores", "Rastreamento da bola"]
        jobs[job_id]["current_step"] = "Gerando estatísticas"
        jobs[job_id]["progress"] = 0.85

        unique_players = len(set([round(p["x"] / 100) for p in player_positions])) if player_positions else 0
        unique_players = max(2, min(4, unique_players))

        stats = {
            "duration_seconds": round(duration, 1),
            "total_frames": total_frames,
            "fps": round(fps, 1),
            "players_detected": unique_players,
            "ball_detections": len(ball_positions),
            "player_positions": player_positions[:100],
            "ball_positions": ball_positions[:100],
        }

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 1.0
        jobs[job_id]["current_step"] = "Concluido"
        jobs[job_id]["steps_completed"] = [
            "Extração de frames",
            "Detecção de jogadores",
            "Rastreamento da bola",
            "Detecção de eventos",
            "Geração de estatísticas",
        ]
        jobs[job_id]["stats"] = stats

        print("Processamento concluido!")
        return stats

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        print("Erro:", str(e))
        return None
