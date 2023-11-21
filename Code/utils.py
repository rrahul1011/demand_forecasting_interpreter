import streamlit as st
import io
from PIL import Image
import base64
import streamlit as st


### Page Configuration
def configure_streamlit_page():
    st.set_page_config(
        page_title="Sigmoid GenAI",
        page_icon="Data/cropped-Sigmoid_logo_3x.png",
        layout="wide",
    )

    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)



def add_contact_info():
    with st.sidebar:
        with st.expander("#### 📧 Contact"):
            st.write("rkushwaha@sigmoidanalytics.com")
    
    

def open_ai_key():
    openai_api_key = st.sidebar.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    col1, col2 = st.sidebar.columns(2)
    m = st.markdown("""
    <style>
    div.stButton {
        display: flex;
        justify-content: flex-end;
    }
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: blue;
        color:#ff0000;
        }
    </style>""", unsafe_allow_html=True)
    submit_button = col1.button("Submit")
    if submit_button:
        # Assign the submitted API key to openai_api_key
        openai_api_key = openai_api_key




## Logo in the side bar
def add_logo():
    # Path to your image
    image_path = "Data/cropped-Sigmoid_logo_3x.png"
    image_width = 250
    image_height = 120
    background_position_x = 0.03
    background_position_y = 0.03

    # Read and resize the image
    file = open(image_path, "rb")
    contents = file.read()
    img_str = base64.b64encode(contents).decode("utf-8")
    buffer = io.BytesIO()
    file.close()
    img_data = base64.b64decode(img_str)
    img = Image.open(io.BytesIO(img_data))
    resized_img = img.resize((image_width, image_height))
    resized_img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

   
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
                background-repeat: no-repeat;
                padding-top: 50px;
                background-position: {background_position_x}px {background_position_y}px;
            }}
            [data-testid="stSidebarNav"]::before {{
                content: "";
                border-bottom: 3px solid crimson;
                width: 100%;
                position: absolute;
                top: 130px; /* Adjust the distance below the image as needed */
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


