
import dlib
import numpy as np 
from sklearn.svm import SVC
import streamlit as st
import face_recognition_models
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()



    sp  = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())


    facerec =  dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp,facerec = load_dlib_models()

    faces =  detector(image_np, 1) 

    encodings=[]

    for face in faces:
        shape = sp(image_np, face)
        face_descriptior  = facerec.compute_face_descriptor(image_np, shape, 1) #128embeddings

        encodings.append(np.array(face_descriptior)) 
    return encodings
  
@st.cache_resource
def get_trained_model():
    X = []
    y = []


    student_db =  get_all_students()

    if not student_db:
        return None 
    
    for student in student_db:
        embeddings =student.get("face_embeddings")
        if embeddings:
            X.append(np.array(embeddings))
            y.append(student.get('student_id'))


    if len(X)==0:
        return 0

    clf  = SVC(kernel="linear",probability=True, class_weight ="balanced" )

    try:
        clf.fit(X,y)

    except ValueError:
        pass

    return {"clf":clf, "X":X,"y":y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return model_data


# def predict_attandance(image_np):
#     encodings =  get_face_embeddings(image_np)

#     detcted_student = {}

#     model_data = get_trained_model()

#     if not model_data:
#         return detcted_student, len(encodings)

#     clf =  model_data["clf"]

#     X_train=model_data["X"]
#     y_train = model_data["y"]

#     all_students = sorted(list(set(y_train)))

#     for encoding in encodings:
#         if len(all_students) >= 2:
#             predicted_id = int(clf.predict([encoding])[0])

#         else:
#             predicted_id = int(all_students[0])

#         student_embeddings = X_train[y_train.index(predicted_id)]

#         best_match_score = np.linalg.norm(student_embeddings  -  encoding)

#         resemblance_score  =  0.6

#         for i, student_embedding in enumerate(X_train):
#             distance = np.linalg.norm(np.array(student_embedding) - encoding)
#             if distance < best_match_score:
#                 best_match_score = distance
#                 best_match_id = y_train[i]

#             if best_match_id is not None and best_match_score <= resemblance_score:
#                 detcted_student[int(best_match_id)] = True

#         return detcted_student, len(encodings)

def predict_attandance(image_np):
    encodings = get_face_embeddings(image_np)

    detcted_student = {}

    model_data = get_trained_model()

    if not model_data:
        return detcted_student,  len(encodings)

    X_train = model_data["X"]
    y_train = model_data["y"]

    # all_students = sorted(list(set(y_train)))
    resemblance_score = 0.6

    for encoding in encodings:
        best_match_id = None
        best_match_score = float("inf")

        for i, student_embedding in enumerate(X_train):
            distance = np.linalg.norm(np.array(student_embedding) - encoding)
            if distance < best_match_score:
                best_match_score = distance
                best_match_id = y_train[i]

        if best_match_id is not None and best_match_score <= resemblance_score:
            detcted_student[int(best_match_id)] = True

    return detcted_student, len(encodings)

