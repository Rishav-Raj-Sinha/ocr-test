import streamlit as st
from PIL import Image
import easyocr
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# page configuration and hide headers/footers
st.set_page_config(page_title="DetectiNator", layout="wide", initial_sidebar_state="collapsed")
hide_decoration_bar_style = '''<style>header {visibility: hidden;}
</style><style>footer{visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)



data = pd.read_csv("Medicine_Details.csv")
#print(data.head())

df_name = "Medicine Name"
medicine_list = data[df_name].dropna().tolist()
df_usage = "Uses"
df_compos = "Composition"
df_se = "Side_effects"

st.title("HealthNet")
col1, col2 = st.columns(2)

with col1 : 
    with st.container(border =True,height = 750):
        with st.container(border = True,height = 620):
            enable = st.checkbox("Enable camera or manually enter the name of prescribed medicine")
            picture = st.camera_input("Take a picture", disabled=not enable)
            if picture :
                #st.image(picture)
                image = Image.open(picture)
                reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
                text = reader.readtext(image,detail = 0)
            #st.write(text[0])
            
        with st.container(border = True,height = 75):
            query = st.chat_input("Enter the name of your prescribed medicine") # "prompt" variable takes the user input
with col2 : 
    with st.container(border =True,height = 750):
      with st.container(border = True,height = 715):
        if picture:
            query = text[0] # "prompt" variable takes the user input
        else:
            query = query 
        if query:
            # query = prompt
            match = process.extractOne(query, medicine_list)

            if match:
                    best_match, score = match

                    matching_indices = data[data[df_name] == best_match].index.tolist()  # list of indices

                    BestMatch = best_match
                    #print("Matching Row Indices:", matching_indices)
                    matching_index = matching_indices[0]
                    composition = (data[df_compos][matching_index])
                    usage = (data[df_usage][matching_index])
                    sideEffects = (data[df_se][matching_index])
                    input = st.chat_message("User")
                    input.write(query )
                    output = st.chat_message("assistant")
                    output.write(f"Hello, the closest match to your medicine is {BestMatch} , it is used for {usage} , and has the following side effects : {sideEffects} , here are the composition(s) of your medicine {composition}") #this line gives the output that is generated using the llm
            else:
                    st.warning("no match found", icon="⚠️")

        
