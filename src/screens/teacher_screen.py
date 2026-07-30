import streamlit as st
from src.components.header import header_dashboard
from src.UI.base_layout  import style_background_dashboard,style_base_layout
from src.components.footer import footer_dashboard
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    # teacher_screen_login()

    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()



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
        st.button("Login", shortcut="control+Enter", type="secondary", icon=":material/passkey:", width='stretch')
    with c3:
        if st.button("Register Insted", type='primary',width='stretch',icon=":material/passkey:"):
            st.session_state.teacher_login_type="register"

    footer_dashboard()






def teacher_screen_register():
    col1, col2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to home", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state["login-type"] = None
            st.rerun()

    st.header("Register your teacher profile",  text_alignment="center")
    st.space()
    st.space()
    teacher_username = st.text_input("Enter Username", placeholder='@Techno' , key="Username")
    teacher_name = st.text_input("Enter name", placeholder='Rahul kumar' , key="Name")
    teacher_password = st.text_input("Enter password", type="password",placeholder="Enter password", key="Password")
    teacher_password_confirm = st.text_input("Confirm password", type="password",placeholder="Confirm password",)

    st.divider()
    c2,c3 = st.columns(2, vertical_alignment="center")
    with c2:
        st.button("Register Now", type='primary',shortcut="control+Enter", icon=":material/passkey:", width='stretch')
    with c3:
       if  st.button("Login Insted",width='stretch',icon=":material/passkey:", type="secondary"):
           st.session_state.teacher_login_type="login"

    footer_dashboard()