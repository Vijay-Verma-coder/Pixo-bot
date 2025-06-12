import streamlit as st
import wikipedia
import requests
from PIL import Image
from io import BytesIO
from gtts import gTTS
import os
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.express as px

# 🎨 Art Forms
ART_FORMS = ["Dance", "Music", "Painting", "Sculpture", "Literature", "Architecture"]

# 🌍 194 Countries + 'World'
COUNTRIES = ["World", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina",
             "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
             "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana",
             "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon",
             "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo",
             "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
             "Dominican Republic", "DR Congo", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea",
             "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany",
             "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras",
             "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast",
             "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",
             "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar",
             "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius",
             "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar",
             "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
             "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea",
             "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
             "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
             "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
             "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan",
             "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan",
             "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
             "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States",
             "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

# 🔊 Greeting when app starts
def play_greeting():
    if not os.path.exists("greeting.mp3"):
        tts = gTTS("Hello! Welcome to Pixo Bot. Let's explore the revolution in art forms!", lang="en")
        tts.save("greeting.mp3")
    with open("greeting.mp3", "rb") as audio:
        st.audio(audio.read(), format="audio/mp3", autoplay=True)

# 📚 Get Wikipedia content and image
def get_info(art, country):
    topic = f"{art} in {country}" if country != "World" else art
    try:
        page = wikipedia.page(topic)
        summary = wikipedia.summary(topic, auto_suggest=False)
        img_url = page.images[0] if page.images else None
    except:
        summary = "No Wikipedia content available for this topic."
        img_url = None
    return summary, img_url

# 🗣 Speak text
def speak_text(text):
    tts = gTTS(text)
    tts.save("speak.mp3")
    with open("speak.mp3", "rb") as f:
        st.audio(f.read(), format="audio/mp3")

# 📈 Fake timeline (demo)
def show_timeline(art, country):
    years = [1200, 1400, 1600, 1800, 1900, 2000, 2025]
    labels = [f"{art} phase {i}" for i in range(1, len(years)+1)]
    fig = px.timeline(
        x_start=[str(years[i]) for i in range(len(years))],
        x_end=[str(years[i+1]) if i+1 < len(years) else "2025" for i in range(len(years))],
        y=labels,
        color=labels,
        title=f"Timeline of {art} in {country}"
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

# 🟪 UI
st.set_page_config(page_title="Pixo Bot", layout="centered")
st.title("🎨 Pixo Bot – Revolution of Art Forms")
play_greeting()

st.markdown("### 📌 Select Art Form and Country")
art = st.selectbox("🎭 Art Form", ART_FORMS)
country = st.selectbox("🌍 Country", COUNTRIES)

if st.button("🔍 Show Revolution"):
    with st.spinner("Fetching from Wikipedia..."):
        summary, img_url = get_info(art, country)
    
    st.subheader("📖 Wikipedia Content")
    st.write(summary)
    
    if img_url:
        try:
            img = Image.open(BytesIO(requests.get(img_url).content))
            st.image(img, caption=f"{art} in {country}", use_column_width=True)
        except:
            st.warning("Image couldn't be loaded.")

    if st.button("🔊 Speak Content"):
        speak_text(summary)

    st.subheader("📆 Timeline")
    show_timeline(art, country)

add_vertical_space(2)
st.markdown("## ❓ Ask Anything")
st.info("Having any query related do ask here")
query = st.text_input("Type your question here...")

if query:
    st.subheader("💬 Answer")
    st.write("This part will use AI if you want it later. Currently offline.")
