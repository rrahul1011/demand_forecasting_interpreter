
import numpy as np 
import pandas as pd
import streamlit as st 
import openai
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader
from utils import add_logo,add_contact_info,configure_streamlit_page,open_ai_key
from function import select_country,country_wise_analysis

##Page Configuration
configure_streamlit_page()
add_logo()
openai_api_key=add_contact_info()
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"]=""
openai_api_key=open_ai_key()
st.session_state["openai_api_key"]=openai_api_key

##Main Content
st.markdown("#### <span style='color: #265B8C;'>Country Insights</span>", unsafe_allow_html=True)
st.markdown("<p style='color: dark grey;'>Your single destination for a comprehensive country overview.</p>", unsafe_allow_html=True)

df_acc= pd.read_excel("Data/accuracy.xlsx")
df_diageo = pd.read_csv("Data/Diageo_gen.csv")
geo=select_country(df_diageo)
st.markdown("---")
col1,col2=st.columns([0.45,0.55])
with col1:
    st.markdown("##### Key Matrics")
    # Accuracy Analysis
    accuracy = 74  
    color = "green" if accuracy > 80 else "red"
    title = "###### 🎯Accuracy Analysis"

    with st.expander(title, expanded=False):
        st.markdown(
            f"<span style='color: #265B8C;'>Percentage Key having Accuracy above 80% for class A and above 70% for class B and C</span> :<span style='color: {color};'>{accuracy}%</span>",
            unsafe_allow_html=True
        )
        st.write(df_acc.reset_index(drop=True).to_markdown())


    ### Negative Forecast Analysis
    title = "###### ➖ Negative Forecast Analysis"
    with st.expander(title, expanded=False):
        st.write("Negative Forecast Analysis")

    ### Flat Forecast Analysis
    title = "###### ☰ Flat Forecast Analysis"
    with st.expander(title, expanded=False):
        st.write("Flat Forecast Analysis")

    ### Channel Sector Overview
    title = "###### 🍻 Channel Sector Overview"
    with st.expander(title, expanded=False):
        st.write("Channel Sector Overview")

    
    
with col2: 
    country_wise_analysis(df_diageo,geo)   

