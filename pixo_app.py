import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO
import time

# ✅ Use new OpenAI client with key from Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

ART_FORMS = ["Music", "Dance", "Painting", "Architecture", "Literature", "Sculpture"]

with open("countries.txt", "r") as f:
    COUNTRIES = [line.strip() for line in f.readlines()]

st.title("🎨 Pixo Bot - Art Revolution Explorer")
st.markdown("<style>div.stTitle {text-align: center;}</style>", unsafe_allow_html=True)

art_form = st.selectbox("Choose an Art Form", ART_FORMS)
country = st.selectbox("Choose a Country", COUNTRIES)

if art_form and country:
    st.markdown(f"### 🤖 Hello! Let’s explore the art revolution of {art_form} in {country}!")

def get_art_revolution_description(art_form, country):
    prompt = f"Explain the historical revolution of {art_form} in {country}, with key points and a timeline."
    resp = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

def get_art_image(art_form, country):
    return f"https://source.unsplash.com/800x400/?{art_form},{country}"

if art_form and country:
    with st.spinner("Fetching art revolution details..."):
        content = get_art_revolution_description(art_form, country)
        img_url = get_art_image(art_form, country)

    st.image(img_url, caption=f"{art_form} in {country}", use_column_width=True)
    st.markdown(f"### 📜 Revolution of {art_form} in {country}")
    st.write(content)

    st.markdown("---")
    st.markdown("### 📅 Timeline")
    st.write("(Timeline included above)")

if art_form and country:
    st.markdown("---")
    st.markdown("### ❓ Ask a follow-up question")
    query = st.text_input("Your question:")

    if query:
        with st.spinner("Thinking..."):
            resp = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": query}]
            )
            st.success(resp.choices[0].message.content)

    st.markdown("---")
    st.markdown("### 🔊 Voice Controls")
    st.warning("Voice not supported on Streamlit Cloud.")
