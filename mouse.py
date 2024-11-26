import cv2
import dlib
import numpy as np
import pygame

# Initialize dlib's face detector (HOG-based) and create the landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Initialize Pygame for mouse control
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Function to calculate midpoint
def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

# Function to get gaze direction
def get_gaze_direction(landmarks):
    left_point = (landmarks.part(36).x, landmarks.part(36).y)
    right_point = (landmarks.part(39).x, landmarks.part(39).y)
    center_top = midpoint(landmarks.part(37), landmarks.part(38))
    center_bottom = midpoint(landmarks.part(41), landmarks.part(40))
    hor_line_length = np.linalg.norm(np.array(left_point) - np.array(right_point))
    ver_line_length = np.linalg.norm(np.array(center_top) - np.array(center_bottom))
    ratio = hor_line_length / ver_line_length
    return ratio

# Function to move mouse
def move_mouse(ratio):
    x, y = pygame.mouse.get_pos()
    if ratio < 1:
        x -= 5
    elif ratio > 1:
        x += 5
    pygame.mouse.set_pos((x, y))

# Main loop
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = landmarks.part(36), landmarks.part(39)
        right_eye = landmarks.part(42), landmarks.part(45)

        for n in range(36, 48):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
        
        ratio = get_gaze_direction(landmarks)
        move_mouse(ratio)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key to break
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
