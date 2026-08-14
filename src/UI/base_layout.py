import streamlit as st 

def style_background_home():
    st.markdown("""
        <style>

            .stApp{
            background:#5865F2 !important;
            }

            .stApp div[data-testid="stColumn"]{
                background-color:#E0E3FF !important;
                padding:2.5rem !important;
                border-radius:5rem !important;
            }

        </style>

""", unsafe_allow_html = True)


def style_background_dashboard():
    st.markdown("""
        <style>
        .stApp{
            background:#E0E3FF !important;
        }


        </style>

""", unsafe_allow_html = True)

def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap');
      @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap');

            #MainMenu, header, footer{
            visibility : hidden
            }

            .block-container{
                padding-top:1.25rem !important;
            }

            h1{
                font-Family: 'Climate Crisis', sans-serif ! important;
                font-size:2.5rem !important;
                line-height:0.9 !important
                margin-bottom:0rem !important; 
            }

         h2{
              font-Family: 'Climate Crisis', sans-serif ! important;
                font-size:2rem !important;
                line-height:1.1 !important
                margin-bottom:0rem !important; 
          }

          h3,h4, p{
          font-family:'Outfit',sans-serif;
          }

        button{
            background:#5566f3 !important;
            color:white !important;
            padding :10px 30px !important;
            border:none !important;
            transition: transform 0.1s ease-in-out !important;
            border-radius:1.5rem !important;
        }

        button[kind="secondary"]{
            border-radius:1.5rem !important;
            background:#EB459E !important;
            # color:black !important;   
            padding :10px 20px !important;
            border :none !important;
            transition: transform 0.1s ease-in-out !important;
          }


        button[kind="tertiary"]{
            border-radius:1.5rem !important;
            background-color:black !important;
            color:white !important;
            padding :10px 20px !important;
            border :none !important;
            transition: transform 0.1s ease-in-out !important;
          }

        button:hover{
          transform:scale(1.05);
        }

   .stApp [data-testid="stImageActionButton"] {
        display: hidden !important;
    }

        </style>

""", unsafe_allow_html = True)