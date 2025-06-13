import streamlit as st
import requests
import wikipedia
from PIL import Image
from io import BytesIO
import pyttsx3
import openai
from datetime import datetime

# ✅ Updated OpenAI setup
client = openai.OpenAI(api_key=st.secrets["openai_key"])

# 🎨 Art Forms
ART_FORMS = ["Music", "Dance", "Painting", "Architecture", "Literature", "Sculpture"]

# 🌍 194 Countries + World
COUNTRIES = ["World", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
    "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil",
    "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic",
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia",
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada",
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
    "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan",
    "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia",
    "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
    "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco",
    "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan",
    "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar",
    "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent", "Samoa",
    "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone",
    "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan",
    "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan",
    "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
    "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States",
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

# 🎉 App UI
st.set_page_config(page_title="Pixo Bot", page_icon="🎨", layout="centered")

st.markdown("## 🤖 Welcome to Pixo Bot!")
st.markdown("### Learn about the Revolution of Art Forms 🌍🎭")
st.markdown("")

# 🎭 Dropdowns
art_form = st.selectbox("🎨 Choose an Art Form", ART_FORMS)
country = st.selectbox("🌍 Choose a Country", COUNTRIES)

# 🎤 Voice greeting
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 😄 Bot Face + Greeting
with st.container():
    st.markdown("### 😊 Hi! I'm Pixo! Let's explore art together.")
    st.image("https://i.imgur.com/VtuZVbI.png", width=100)

# 🔍 Wikipedia + Image
def get_content_and_image(art_form, country):
    topic = f"{art_form} in {country}" if country != "World" else f"{art_form} in the world"
    try:
        summary = wikipedia.summary(topic, sentences=10)
    except:
        summary = f"Sorry, I couldn't find detailed information about {art_form} in {country}."

    try:
        page = wikipedia.page(topic)
        image_url = page.images[0] if page.images else None
    except:
        image_url = None

    return summary, image_url

# 🖼️ Display Results
if art_form and country:
    st.markdown(f"### 📜 Revolution of {art_form} in {country}")
    summary, img_url = get_content_and_image(art_form, country)
    st.write(summary)

    if img_url:
        image = Image.open(BytesIO(requests.get(img_url).content))
        st.image(image, use_column_width=True)

    # 🕰️ Timeline (Simple Version)
    st.markdown("### ⏳ Timeline of Evolution")
    st.markdown(f"- **Ancient Period** – Early roots of {art_form}")
    st.markdown(f"- **Medieval Era** – Growth through kingdoms/empires")
    st.markdown(f"- **Modern Age** – Major revolutions and global spread")
    st.markdown(f"- **Present Day** – {art_form} in current culture")

    # 🗣️ Speak content
    if st.button("🔊 Speak Summary"):
        speak(summary)

# 🧠 AI Query Box
st.markdown("### 💬 Having any query related do ask here")
user_input = st.text_input("Ask about the revolution of art forms (after selecting above):")

# 🔊 Voice controls
if user_input:
    st.markdown("🤖 Thinking...")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are an expert in the history and revolution of art. Only answer about {art_form} in {country}."},
            {"role": "user", "content": user_input}
        ]
    )
    final_answer = response.choices[0].message.content
    st.markdown("### 🤖 Pixo Says:")
    st.write(final_answer)

    if st.button("🗣 Speak Answer"):
        speak(final_answer)
