import os
import streamlit as st
import base64
from openai import OpenAI
import openai
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

Expert=" "
profile_imgenh=" "

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

st.set_page_config(page_title='Tablero Inteligente', layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #A4E055 !important;
        }
        .stApp {
            background-color: #A4E055;
            color: black;
            text-align: center;
        }
        .stTextInput > div > div > input {
            text-align: center;
            color: black !important;
        }
        .stButton button {
            display: block;
            margin: 0 auto;
            color: white !important;
        }
        .stSlider {
            text-align: center;
        }
        .stMarkdown {
            text-align: center !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: black;'>Tablero Inteligente</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #A4E055;'>Acerca de:</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #A4E055;'>En esta aplicación veremos la capacidad que ahora tiene una máquina de interpretar un boceto</h4>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: black;'>Dibuja el boceto en el panel  y presiona el botón para analizarla</h4>", unsafe_allow_html=True)

drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
stroke_color = "#000000" 
bg_color = '#FFFFFF'

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

ke = st.text_input('Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

analyze_button = st.button("Analiza la imagen", type="secondary")

if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')

        base64_image = encode_image_to_base64("img.png")
        prompt_text = (f"Describe in spanish briefly the image")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url":f"data:image/png;base64,{base64_image}",
                    },
                ],
            }
        ]

        try:
            full_response = ""
            message_placeholder = st.empty()
            response = openai.chat.completions.create(
              model= "gpt-4o-mini",
              messages=[
                {
                   "role": "user",
                   "content": [
                     {"type": "text", "text": prompt_text},
                     {
                       "type": "image_url",
                       "image_url": {
                         "url": f"data:image/png;base64,{base64_image}",
                       },
                     },
                   ],
                  }
                ],
              max_tokens=500,
              )
            if response.choices[0].message.content is not None:
                    full_response += response.choices[0].message.content
                    message_placeholder.markdown(f"<div style='text-align: center; color: black;'>{full_response}▌</div>", unsafe_allow_html=True)
            message_placeholder.markdown(f"<div style='text-align: center; color: black;'>{full_response}</div>", unsafe_allow_html=True)
            if Expert== profile_imgenh:
               st.session_state.mi_respuesta= response.choices[0].message.content 
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    if not api_key:
        st.warning("Por favor ingresa tu API key.")
