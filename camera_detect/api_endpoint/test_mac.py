from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import numpy as np
import cv2
import mediapipe as mp
import time
import io
from PIL import Image

app = FastAPI(
    title="Face Recognition API",
    description="API for face pose detection and login verification (Docker Compatible)"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MediaPipe and cascades once at startup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
smile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_smile.xml'
)

# Session state (in production, use Redis or database)
session_state = {
    "login_seq": ["Looking Left", "Looking Right", "Looking Up", "Smile"],
    "current_step": 0,
    "login_finished": False,
    "hold_time": 1.0,
    "pose_start_time": None,
    "last_pose": "Unknown"
}


def detect_pose(image):
    """Detect face pose from image"""
    img_h, img_w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    pose = "Unknown"
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            face_2d, face_3d = [], []
            
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [33, 263, 1, 61, 291, 199]:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    face_2d.append([x, y])
                    face_3d.append([x, y, lm.z])
            
            if len(face_2d) >= 6:
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)
                
                focal_length = img_w
                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                     [0, focal_length, img_w / 2],
                                     [0, 0, 1]])
                distortion_matrix = np.zeros((4, 1), dtype=np.float64)
                
                success, rotation_vec, translation_vec = cv2.solvePnP(
                    face_3d, face_2d, cam_matrix, distortion_matrix
                )
                
                if success:
                    rmat, _ = cv2.Rodrigues(rotation_vec)
                    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
                    
                    x_angle = angles[0] * 360
                    y_angle = angles[1] * 360
                    
                    if y_angle < -3:
                        pose = "Looking Left"
                    elif y_angle > 3:
                        pose = "Looking Right"
                    elif x_angle > 3:
                        pose = "Looking Up"
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(
            roi_gray, scaleFactor=1.8, minNeighbors=20, minSize=(25, 25)
        )
        if len(smiles) > 0:
            pose = "Smile"
    
    return pose


def process_login_step(pose):
    """Process current login step"""
    state = session_state
    
    if not state["login_finished"]:
        expected = state["login_seq"][state["current_step"]]
        
        if pose == expected:
            if state["pose_start_time"] is None:
                state["pose_start_time"] = time.time()
            elif time.time() - state["pose_start_time"] >= state["hold_time"]:
                state["current_step"] += 1
                state["pose_start_time"] = None
                if state["current_step"] >= len(state["login_seq"]):
                    state["login_finished"] = True
        else:
            state["pose_start_time"] = None
    
    state["last_pose"] = pose


def add_overlay_text(image, pose):
    """Add text overlay to image"""
    state = session_state
    
    if not state["login_finished"]:
        expected = state["login_seq"][state["current_step"]]
        cv2.putText(image, f"Do: {expected}", (20, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        
        progress = f"{state['current_step']}/{len(state['login_seq'])}"
        cv2.putText(image, f"Progress: {progress}", (20, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    else:
        cv2.putText(image, "Login Successful!", (20, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    
    cv2.putText(image, f"Pose: {pose}", (20, 420),
               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
    
    return image


@app.post("/api/face/process")
async def process_frame(file: UploadFile = File(...)):
    """
    Process a single frame sent from frontend.
    Frontend captures camera, sends frame here for processing.
    WORKS IN DOCKER!
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image")
        
        # Detect pose
        pose = detect_pose(image)
        
        # Process login step
        process_login_step(pose)
        
        # Add overlay
        image = add_overlay_text(image, pose)
        
        # Encode back to JPEG
        ret, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ret:
            raise HTTPException(status_code=500, detail="Failed to encode image")
        
        return StreamingResponse(
            io.BytesIO(buffer.tobytes()),
            media_type="image/jpeg"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/face/detect")
async def detect_only(file: UploadFile = File(...)):
    """
    Just detect pose without processing login sequence.
    Returns JSON with pose information.
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image")
        
        pose = detect_pose(image)
        
        return {
            "pose": pose,
            "timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/face/status")
async def get_login_status():
    """Get current login verification status"""
    state = session_state
    return {
        "current_step": state["current_step"],
        "total_steps": len(state["login_seq"]),
        "current_pose_required": state["login_seq"][state["current_step"]] if state["current_step"] < len(state["login_seq"]) else None,
        "login_finished": state["login_finished"],
        "progress_percentage": (state["current_step"] / len(state["login_seq"])) * 100,
        "last_pose": state["last_pose"]
    }


@app.post("/api/face/reset")
async def reset_login():
    """Reset the login verification process"""
    state = session_state
    state["current_step"] = 0
    state["login_finished"] = False
    state["pose_start_time"] = None
    state["last_pose"] = "Unknown"
    
    return {"message": "Login process reset successfully"}


@app.get("/api/face/sequence")
async def get_login_sequence():
    """Get the required pose sequence for login"""
    return {
        "sequence": session_state["login_seq"],
        "hold_time": session_state["hold_time"]
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Face Recognition API (Docker Compatible)",
        "note": "Frontend must capture camera and send frames to /api/face/process",
        "endpoints": {
            "process_frame": "POST /api/face/process - Process frame with overlay",
            "detect_only": "POST /api/face/detect - Detect pose only (JSON)",
            "status": "GET /api/face/status",
            "reset": "POST /api/face/reset",
            "sequence": "GET /api/face/sequence"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)