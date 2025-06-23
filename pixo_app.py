import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

# ✅ Set your API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# ✅ Art forms and countries
ART_FORMS = ["Music", "Dance", "Painting", "Architecture", "Literature", "Sculpture"]

# ✅ Load countries from countries.txt
with open("countries.txt", "r") as f:
    COUNTRIES = [line.strip() for line in f.readlines()]

# ✅ Title and dropdowns
st.title("🎨 Pixo Bot - Art Revolution Explorer")
art_form = st.selectbox("Choose an Art Form", ART_FORMS)
country = st.selectbox("Choose a Country", COUNTRIES)

# ✅ Greeting
if art_form and country:
    st.markdown(f"### 🤖 Let’s explore the {art_form} revolution in {country}!")

# ✅ Function to get description
def get_art_revolution_description(art_form, country):
    prompt = f"Give a simplified, clear explanation of the historical revolution of {art_form} in {country}, with important points and a timeline."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ✅ Image from Unsplash
def get_art_image(art_form, country):
    url = f"https://source.unsplash.com/800x400/?{art_form},{country}"
    return url

# ✅ Display content
if art_form and country:
    with st.spinner("Fetching revolution details..."):
        content = get_art_revolution_description(art_form, country)
        image_url = get_art_image(art_form, country)

    st.image(image_url, caption=f"{art_form} in {country}", use_column_width=True)
    st.markdown("### 📜 Art Revolution Summary")
    st.write(content)

    # ✅ Timeline section
    st.markdown("---")
    st.markdown("### 📅 Timeline")
    st.write("(Included in the explanation above)")

# ✅ Query box
if art_form and country:
    st.markdown("---")
    st.markdown("### ❓ Ask anything about this art revolution")
    st.markdown("Having any query related do ask here 🗣️")
    query = st.text_input("Your Question:")

    if query:
        with st.spinner("Thinking..."):
            followup = f"You're an expert in art history. Based on {art_form} in {country}, answer: {query}"
            reply = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": followup}]
            )
            st.success(reply.choices[0].message.content)

    # ✅ Voice controls (disabled for Streamlit Cloud)
    st.markdown("---")
    st.markdown("### 🔊 Voice Controls")
    if st.button("Speak Answer"):
        st.warning("🔈 Voice not supported on Streamlit Cloud.")
    if st.button("Pause"):
        st.warning("⏸️ Pause not available on Streamlit Cloud")
    if st.button("Stop"):
        st.warning("⏹️ Stop not available on Streamlit Cloud")
