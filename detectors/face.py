import cv2
import dlib

detector = dlib.get_frontal_face_detector()

def face_detector(image):
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(frame)
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x, y), (x1, y1), (8, 8, 136), 4)
    cv2.imshow("Frame", frame)
    