from src.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def checkPass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(),hashed.encode())

def check_teacher_exists(username):
    # Check for unique username , returns false when username  already taken;
    response =  supabase.table("teachers").select('username').eq("username", username).execute()
    return len(response.data) > 0



   
def create_teacher(username, password, name):
    
    data =  {
        "username":username,
        "password": hash_pass(password),
        "name":name
    }
    response  =  supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username, password):
    response =  supabase.table("teachers").select('*').eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if checkPass(password, teacher['password']):
            return teacher
    return None
        

def get_all_students():
    response  = supabase.table("students").select("*").execute()
    return response.data


def create_student(new_name, face_embeddings=None, voice_embeddings=None):
    data= {
        'name':new_name,
        'face_embeddings':face_embeddings,
        'voice_embeddings': voice_embeddings
    }

    response= supabase.table('students').insert(data).execute()
    return response.data



def create_subject(subject_code, name, section, teacher_id):
    data={
        'subject_code':subject_code,
        'name':name,
        'section':section,
        'teacher_id':teacher_id
    }
    response =  supabase.table("subjects").insert(data).execute()
    return response.data


def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attandance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects =  response.data


    for sub in subjects:
        sub["total_students"] =  sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attandance =  sub.get("attandance_logs",[])
        unique_session  = len(set(log["timestamp"] for log in attandance))
        sub["total_classes"]  = unique_session 

        sub.pop("subjects_student", None)
        sub.pop("attandance_logs", None)

    return subjects


def enroll_student_to_subject(student_id , subject_id):
    data= {
        'student_id':student_id,
        'subject_id':subject_id
    }
    res  = supabase.table("subject_students").insert(data).execute()

    return res.data

def unenroll_student_to_subject(student_id, subject_id):
    res  = supabase.table("subject_students").delete().eq('student_id', student_id).eq('subject_id', subject_id ).execute()
    return res.data 

def get_student_subject(student_id):
    response  =  supabase.table("subject_students").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data

def get_student_attendance(student_id):
    response  = supabase.table("attandance_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data


def create_attendace(logs):
    response =  supabase.table("attandance_logs").insert(logs).execute()
    return response.data



def get_attendance_for_teacher(teacher_id):
    response =  supabase.table('attandance_logs').select('*, subjects!inner(*)').eq('subjects.teacher_id',teacher_id).execute()
    return response.data 
