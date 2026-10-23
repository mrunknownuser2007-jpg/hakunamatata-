import os
import shutil
from deepface import DeepFace

FACE_DB = "face_db"
MODEL = "Facenet512"
os.makedirs(FACE_DB, exist_ok=True)
os.makedirs("temp", exist_ok=True)

def register_face(image_path, rollno):
    """Student register karte time uska face save karna"""
    try:
        dest = os.path.join(FACE_DB, f"{rollno}.jpg")
        shutil.copy(image_path, dest)
        print(f"Face registered: {rollno} -> {dest}")
        return True
    except Exception as e:
        print(f"Register error: {e}")
        return False

def recognize_face(image_path):
    """Attendance ke time face match karna"""
    try:
        if not os.path.exists(FACE_DB) or len(os.listdir(FACE_DB)) == 0:
            print("No faces in DB")
            return None

        # face_db folder me se match dhundho
        dfs = DeepFace.find(
            img_path=image_path,
            db_path=FACE_DB,
            model_name=MODEL,
            enforce_detection=False,
            silent=True
        )
        
        if len(dfs) > 0 and not dfs[0].empty:
            # sabse pehla match le lo
            matched_path = dfs[0].iloc[0]['identity']
            rollno = os.path.splitext(os.path.basename(matched_path))[0]
            print(f"Face matched: {rollno}")
            return rollno
        else:
            print("No face matched")
            return None

    except Exception as e:
        print(f"Recognize error: {e}")
        return None