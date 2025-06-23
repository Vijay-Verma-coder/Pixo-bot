import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO
import time

# ✅ Secure API key from secrets.toml
openai.api_key = st.secrets["openai"]["api_key"]

# ✅ Art forms and countries
ART_FORMS = ["Music", "Dance", "Painting", "Architecture", "Literature", "Sculpture"]

# ✅ Load countries list from file (make sure you uploaded 'countries.txt')
with open("countries.txt", "r") as f:
    COUNTRIES = [line.strip() for line in f.readlines()]

# ✅ Title and dropdowns
st.title("🎨 Pixo Bot - Art Revolution Explorer")
st.markdown("<style>div.stTitle {text-align: center;}</style>", unsafe_allow_html=True)

art_form = st.selectbox("Choose an Art Form", ART_FORMS)
country = st.selectbox("Choose a Country", COUNTRIES)

# ✅ Auto greeting
if art_form and country:
    st.markdown(f"### 🤖 Hello! Let’s explore the art revolution of {art_form} in {country}!")

# ✅ Function to fetch description
def get_art_revolution_description(art_form, country):
    prompt = f"Give a simplified, clear explanation of the historical revolution of {art_form} in {country}, with important points and a timeline."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ✅ Function to get image from Unsplash
def get_art_image(art_form, country):
    search_term = f"{art_form} in {country}"
    url = f"https://source.unsplash.com/800x400/?{search_term}"
    return url

# ✅ Display fetched data
if art_form and country:
    with st.spinner("Fetching art revolution details..."):
        content = get_art_revolution_description(art_form, country)
        img_url = get_art_image(art_form, country)

    st.image(img_url, caption=f"{art_form} in {country}", use_column_width=True)
    st.markdown(f"### 📜 Revolution of {art_form} in {country}")
    st.write(content)

    # ✅ Timeline section
    st.markdown("---")
    st.markdown("### 📅 Timeline")
    st.write("(Timeline details included in the explanation above)")

# ✅ Query Section
if art_form and country:
    st.markdown("---")
    st.markdown("### ❓ Ask me anything about this art revolution")
    st.markdown("Having any query related do ask here 🗣️")
    query = st.text_input("Your Question:")

    if query:
        with st.spinner("Thinking..."):
            followup = f"You are an expert on art revolutions. Based on earlier, answer this related question clearly: {query}"
            reply = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": followup}]
            )
            answer = reply.choices[0].message.content
            st.success(answer)

        # ✅ Voice Controls (not supported on Streamlit Cloud)
        st.markdown("---")
        st.markdown("### 🔊 Voice Controls")
        if st.button("Speak Answer"):
            st.warning("🔈 Voice not supported on Streamlit Cloud.")
        if st.button("Pause"):
            st.warning("⏸️ Pause not available on Streamlit Cloud")
        if st.button("Stop"):
            st.warning("⏹️ Stop not available on Streamlit Cloud")
