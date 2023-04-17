import os

import cv2
import dlib
import numpy as np
from skimage import io
from utils import speak

data_dir = os.path.expanduser("./data")
faces_folder_path = "./known_faces/"
dlib_frontal_face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(
    data_dir + "/shape_predictor_68_face_landmarks.dat"
)
face_recognition_model = dlib.face_recognition_model_v1(
    data_dir + "/dlib_face_recognition_resnet_model_v1.dat"
)
face_detector = dlib.get_frontal_face_detector()


def get_face_encodings(face):
    bounds = face_detector(face, 1)
    faces_landmarks = [shape_predictor(face, face_bounds) for face_bounds in bounds]
    return [
        np.array(face_recognition_model.compute_face_descriptor(face, face_pose, 1))
        for face_pose in faces_landmarks
    ]


def get_face_matches(known_faces, face):
    return np.linalg.norm(known_faces - face, axis=1)


def find_match(known_faces, person_names, face):
    matches = get_face_matches(known_faces, face)
    min_index = matches.argmin()
    min_value = matches[min_index]
    if min_value < 0.55:
        return person_names[min_index] + "! ({0:.2f})".format(min_value)
    if min_value < 0.58:
        return person_names[min_index] + " ({0:.2f})".format(min_value)
    if min_value < 0.65:
        return person_names[min_index] + "?" + " ({0:.2f})".format(min_value)
    return "Not Found"


def load_face_encodings(faces_folder_path):
    image_filenames = filter(
        lambda x: x.endswith(".jpg"), os.listdir(faces_folder_path)
    )
    image_filenames = sorted(image_filenames)
    person_names = [x[:-4] for x in image_filenames]
    full_paths_to_images = [faces_folder_path + x for x in image_filenames]
    face_encodings = []
    for path_to_image in full_paths_to_images:
        face = io.imread(path_to_image)
        faces_bounds = face_detector(face, 1)
        if len(faces_bounds) != 1:
            print(
                "Expected one and only one face per image: "
                + path_to_image
                + " - it has "
                + str(len(faces_bounds))
            )
            continue
        face_bounds = faces_bounds[0]
        face_landmarks = shape_predictor(face, face_bounds)
        face_encoding = np.array(
            face_recognition_model.compute_face_descriptor(face, face_landmarks, 1)
        )
        face_encodings.append(face_encoding)
    return face_encodings, person_names


face_encodings, person_names = load_face_encodings(faces_folder_path)


def recognize_faces_in_frame(frame):
    faceClassifier = cv2.CascadeClassifier(
        data_dir + "/haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_rects = faceClassifier.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    for x, y, w, h in face_rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_encodings_in_image = get_face_encodings(frame)
        if face_encodings_in_image:
            match = find_match(face_encodings, person_names, face_encodings_in_image[0])
            cv2.putText(
                frame,
                match,
                (x + 5, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
            )
            name = match.split("!")[0]
            certinity = match.split("! (")[1].split(")")[0]
            if name != prev_match:
                speak(f"Its {name} with Certinity of {certinity}!")
