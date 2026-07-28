import streamlit as st 
from src.components.header import get_image_src
def footer_home():
    logo = get_image_src("src/images/my_name.png")
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; align-item:center; margin-top:20px; ">
        <p style="font-size:1.25rem; padding-top:0.5rem; font-weight:bold; color:white; ">Made with ❤️ by &nbsp;<p/>
        <img src='{logo}' style="max-height:50px;"/>
        </div>
""", unsafe_allow_html=True)