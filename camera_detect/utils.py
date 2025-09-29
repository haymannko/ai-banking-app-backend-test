import cv2 
from api_endpoint import model_cam 

cam = model_cam.OpenCam()
while cam.cap.isOpened():
    success, image = cam.cap.read()
    if not success:
        break
    
    image = cv2.flip(image, 1)
    pose = cam.detect_pose(image)
    cam.process_login_step(pose)
    image = cam.add_overlay_text(image, pose)
    
    cv2.imshow('Login Challenge', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
    
    cam.release()