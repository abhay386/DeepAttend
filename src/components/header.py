import base64
import streamlit as st 

def get_image_src(path:str)->str :
    try:
        with open(path, "rb") as r:
            data= r.read()
            encoded = base64.b64encode(data).decode()
            return  f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        return ""

def header_home():

    logo_url = get_image_src("src/images/attandace_logo.png")
    st.markdown(
        f"""
    <div style='display:flex; flex-direction:column; align-items:center; justify-content:center;margin-bottom:20px;margin-top:20px;'>
        <img src='{logo_url}' style='height:90px;'>
        <h1 style='text-align:center; color:#dfe2fc'>Deep<br/> Attend</h1>
    </div>
        """, 
        unsafe_allow_html=True
    )
