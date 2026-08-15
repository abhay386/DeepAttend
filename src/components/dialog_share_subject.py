import streamlit as st 
import segno 
import io 

@st.dialog("Share subject Link")
def share_subject_dialog(name, subject_code):
    app_domain = "deep-attend-main.streamlit.app"
    join_url =  f"{app_domain}?join-code={subject_code}"

    st.header("Scan to join")

    qr =  segno.make(join_url)

    out =  io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 =  st.columns(2)

    with col1:
        st.markdown('### copy code')
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info("Copy this to share on Whatsapp or Email")

    with col2:
        st.markdown('### copy code')
        st.image(out.getvalue(), caption ="ORCODE for class joining")
