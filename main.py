import streamlit as st
from PIL import Image
import easyocr

picture = st.camera_input("Take a picture")
if picture :
        st.image(picture)
        image = Image.open(picture)
        reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
        text = reader.readtext(image,detail = 0)
        st.write(text[0])
