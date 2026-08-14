import streamlit as st
from src.components.header import header_dashboard
from src.UI.base_layout  import style_background_dashboard,style_base_layout
from src.components.footer import footer_dashboard
from src.database.db import create_teacher, check_teacher_exists, teacher_login,get_teacher_subjects,get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.add_photo_dialog import add_photos_dialog
from src.pipelines.face_pipeline import predict_attandance
from datetime import datetime
from src.components.dialog_attendance_results import attendance_result_dialog
import pandas as pd 
import numpy as np
from src.database.config import supabase

from src.components.dialog_voice_attendance import dialog_voice_attendance
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    # teacher_screen_login()
    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data =  st.session_state.teacher_data
    col1, col2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    with col1:
        header_dashboard()
    with col2:
        st.header(f"Welcome, {teacher_data['name']}")
        if st.button("Logout", type="secondary", key="logoutbackbtn", shortcut="control+backspace"):
            st.session_state["login-type"] = False 
            del st.session_state.teacher_data
            st.rerun()

    st.space()
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab =  "take_attendance"
        
    tab1, tab2, tab3 =  st.columns(3)

    with tab1:
        type1 = 'primary' if st.session_state.current_teacher_tab == "take_attendance" else 'tertiary'
        if st.button("Take Attandance", width="stretch", icon=":material/ar_on_you:",type = type1):
            st.session_state.current_teacher_tab =  "take_attendance"
            st.rerun()

    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == "manage_subjects" else 'tertiary'
        if st.button("Manage subjects", width="stretch", icon=":material/book_ribbon:",type = type2, key="manage"):
            st.session_state.current_teacher_tab =  "manage_subjects"
            st.rerun()

    with tab3:
       type3 =  'primary' if st.session_state.current_teacher_tab == "attandance_records" else  "tertiary"
       if st.button("Attendance Records ",width="stretch", icon=":material/cards_stack:", type = type3, key="records"):
            st.session_state.current_teacher_tab =  "attandance_records"
            st.rerun()


    st.divider()
           
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attandance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attandance_records":
        teacher_tab_attandance_records()


    footer_dashboard()

def teacher_tab_take_attandance():
    
    teacher_id =  st.session_state.teacher_data["teacher_id"]
    st.header("Take Attandace")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("You haven't created any subjects yet! Please create one to begin!")
        return 

    subjects_options = {f"{s['name']}-{s['subject_code']}": s['subject_id'] for s in subjects}

    col1 ,col2=  st.columns([3,1], vertical_alignment='bottom')
 
    with col1:
        selected_subject_label  =  st.selectbox("Select Subject", options=list(subjects_options.keys()))

    with col2:
        if st.button("Add photos", type='primary',icon=":material/photo_prints:", width='stretch'):
            add_photos_dialog()

    selected_subject_id =  subjects_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header("Added Images")
        gallery_cols = st.columns(4)

        for idx, img  in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption=f"Photo {idx+1}")

    has_photos =  bool(st.session_state.attendance_images)
    c1,c2, c3 =  st.columns(3)

    with c1:
       if st.button("Clear All photos", width='stretch', key='clear',type="tertiary", icon=":material/delete:", disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if  st.button("Run face analysis ", width='stretch', type='secondary', icon=":material/analytics:", disabled= not has_photos):
            with st.spinner("Deep scanning classroom photos..."):

                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    np_img = np.array(img.convert('RGB'))
                    detected,_,_ =  predict_attandance(np_img)


                    if detected:
                        for sid in detected.keys():
                            student_id= int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res =  supabase.table('subject_students').select('*, students(*)').eq('subject_id',selected_subject_id ).execute()

                enrolled_students  =  enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this course")

                else:
                    results, attendance_to_log = [],[]

                    current_timestamp  = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                    for node in enrolled_students:
                        student =  node['students']
                        sources =  all_detected_ids.get(int(student['student_id']),[])
                        is_present =  len(sources) > 0


                        results.append({
                            "Name":student["name"],
                            "ID":student['student_id'],
                            "Sources":",".join(sources) if is_present else "_",
                            "Status":"✅ Present" if is_present else "❌ Absent",
                        })

                        attendance_to_log.append({
                            'student_id': student["student_id"],
                            'subject_id':selected_subject_id,
                            'timestamp':current_timestamp,
                            'is_present':bool(is_present)
                        })

            attendance_result_dialog(pd.DataFrame(results),attendance_to_log)

    with c3:
      if st.button("Voice Attendance", width='stretch',icon=':material/mic:', type='primary'):
          dialog_voice_attendance(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id =  st.session_state.teacher_data["teacher_id"]

    col1, col2 =  st.columns(2)
    with col1:
        st.header("Mangae subjects")

    with col2:
       if st.button("Create new subject",width="stretch"):
           create_subject_dialog(teacher_id)


    # List all subjects 
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥","Students", sub["total_students"]),
                ("🕰️", "Classes", sub["total_classes"])
            ]
        def share_button():
            if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                share_subject_dialog(sub['name'], sub['subject_code'])
                st.space()

        subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats=stats,
                footer_callback=share_button  
        )
    else:
        st.info("NO SUBJECTS FOUND . CREATE ONE ABOVE")




def teacher_tab_attandance_records():
    st.header('Attendance Records')
    teacher_id = st.session_state.teacher_data['teacher_id']
    
    records  = get_attendance_for_teacher(teacher_id)

    data  = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group":ts.split(".")[0] if ts else None,
            "Time":datetime.fromisoformat(ts).strftime('%Y-%m-%d %I:%M %p') if ts else 'N/A',
            "Subject":r["subjects"]["name"],
            "Subject Code": r['subjects']['subject_code'],
            "is_present":bool(r.get('is_present', False))
        })

        df  = pd.DataFrame(data)

        summary  = (
            df.groupby(['ts_group','Time','Subject','Subject Code','is_present'])
            .agg(
                present_count = ('is_present','sum'),
                Total_Count = ('is_present', 'count')
            ).reset_index()
        )

        summary['Attendance Stats'] = (
            "✅" +summary['present_count'].astype(str)+"/"
            +summary['Total_Count'].astype(str)+'Students'
        )

        display_df =(summary.sort_values(by='ts_group', ascending =False)
                    [['Time', 'Subject','Subject Code','Attendance Stats']]
        )

        st.dataframe(display_df, width='stretch', hide_index=True)




def login_teacher(username, password):
    if not username or not password:
        return False 
    teacher =  teacher_login(username, password)

    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data =  teacher
        st.session_state.is_logged_in =  True
        return True
def teacher_screen_login():
    col1, col2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to home", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state["login-type"] = None
            st.rerun()

    st.header("Login using password",  text_alignment="center")
    st.space()
    st.space()
    teacher_username = st.text_input("Enter Username", placeholder='@Techno', key="username")
    teacher_pass = st.text_input("Enter password", placeholder="Enter password", key="passwod",type="password")

    st.divider()
    c2,c3 = st.columns(2, vertical_alignment="center")
    with c2:
      if st.button("Login", shortcut="control+Enter", type="secondary", icon=":material/passkey:", width='stretch'):
        if login_teacher(teacher_username, teacher_pass):
            st.toast("Welcome Back!", icon="👏")
            import time 
            time.sleep(2)
            st.rerun()
        else:
            st.error('Invalid username or password')
          
    with c3:
        if st.button("Register Insted", type='primary',width='stretch',icon=":material/passkey:"):
            st.session_state.teacher_login_type="register"

    footer_dashboard()


def teacher_register(teacher_username, teacher_name, teacher_pass, teacher_confirm_pass):
    if not teacher_username or not teacher_pass or not  teacher_name:
        return False, "All feilds required"
    if check_teacher_exists(teacher_username):
        return False,"Username Already taken"
    if teacher_pass != teacher_confirm_pass:
        return False, "password dosen't match"
    try:
        create_teacher(teacher_username, teacher_pass,teacher_name)
        return True , "Succesfully Created! Login Now"
    except Exception as e :
        return False, 'Unexpected Error'



def teacher_screen_register():
    col1, col2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to home", type="secondary", key="loginbackbtn1", shortcut="control+backspace"):
            st.session_state["login-type"] = None
            st.rerun()

    st.header("Register your teacher profile",  text_alignment="center")
    st.space()
    st.space()
    teacher_username = st.text_input("Enter Username", placeholder='@Techno' , key="Username")
    teacher_name = st.text_input("Enter name", placeholder='Rahul kumar' , key="Name")
    teacher_pass = st.text_input("Enter password", type="password",placeholder="Enter password", key="Password")
    teacher_confirm_pass = st.text_input("Confirm password", type="password",placeholder="Confirm password")

    st.divider()
    c2,c3 = st.columns(2, vertical_alignment="center")
    with c2:
        if st.button("Register Now", type='primary',shortcut="control+Enter", icon=":material/passkey:", width='stretch'):
            success, message = teacher_register(teacher_username, teacher_name, teacher_pass, teacher_confirm_pass)
            if success:
                st.success(message)
                import time 
                time.sleep(2)
                st.session_state.teacher_login_type ="login" 
                st.rerun()
            else:
                st.error(message)
    with c3:
       if  st.button("Login Insted",width='stretch',icon=":material/passkey:", type="secondary"):
           st.session_state.teacher_login_type="login"

    footer_dashboard()