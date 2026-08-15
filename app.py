import streamlit as st 
from  src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.home_screen import home_screen
from src.components.auto_enroll_dialog import auto_enroll_dialog
def main():

    st.set_page_config(
        page_title="DeepAttend- Making Attendance faster using AI",
        page_icon='https://i.ibb.co/844D9Lrt/mascot-student.png'
    )
    if 'login-type' not in st.session_state:
        st.session_state['login-type'] = None

    # st.write(st.session_state['login-type'])

    match st.session_state['login-type'] :
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()
        case _:
            st.session_state['login-type'] = None
            st.rerun()
        

    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state['login-type'] != 'student':
            st.session_state['login-type'] = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

main()
