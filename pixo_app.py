import streamlit as st
import requests
from gtts import gTTS
from io import BytesIO
import base64
import plotly.graph_objects as go
import openai
import random

# 🔧 Page Setup
st.set_page_config(page_title="Pixo Bot", layout="centered")
st.markdown("""
    <style>
        .main {background-color: #fffafc;}
        .block-container {
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        .stButton button {
            border-radius: 10px;
            background-color: #7b2cbf;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# 🔑 OpenAI Key
openai.api_key = st.secrets["openai_key"]

# 🌍 Country and Art Forms
ART_FORMS = ["Music", "Dance", "Painting", "Architecture", "Literature", "Sculpture"]
COUNTRIES = ["World", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

# 👋 Auto Greeting with Expression
if 'greeted' not in st.session_state:
    greeting = "Hello! I'm Pixo Bot. Let's explore the evolution of art around the globe!"
    tts = gTTS(text=greeting, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    st.image("https://i.imgur.com/lRdM6Ok.png", width=120)  # Emoji face
    st.audio(mp3_fp.getvalue(), format='audio/mp3')
    st.session_state['greeted'] = True

# 🎯 Selections
country = st.selectbox("🌍 Choose a Country", COUNTRIES)
art_form = st.selectbox("🎨 Choose an Art Form", ART_FORMS)

# ✍️ OpenAI Content
st.subheader(f"📜 Revolution of {art_form} in {country}")
prompt = f"Give a long, simple, and detailed explanation of the historical revolution and evolution of {art_form} in {country}."
with st.spinner("Generating from AI..."):
    reply = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful historian bot that explains the revolution of global art forms in a clear and long way."},
            {"role": "user", "content": prompt}
        ]
    )
    content = reply.choices[0].message.content
    st.write(content)

# 🔊 Speak and Pause
if st.button("🔈 Speak"):
    tts_content = gTTS(text=content, lang='en')
    voice_fp = BytesIO()
    tts_content.write_to_fp(voice_fp)
    st.audio(voice_fp.getvalue(), format='audio/mp3')

# 🖼️ Relevant Image (Google Style)
st.subheader("🖼️ Visual Art")
st.image(f"https://source.unsplash.com/900x400/?{art_form},{country},art", use_column_width=True)

# 🕰️ Timeline Chart
st.subheader("📊 Timeline of Evolution")
years = [1700, 1750, 1800, 1850, 1900, 1950, 2000, 2020]
progress = [random.randint(1, 10) for _ in years]
fig = go.Figure(go.Scatter(x=years, y=progress, mode='lines+markers', line=dict(color='indigo')))
fig.update_layout(xaxis_title="Year", yaxis_title="Cultural Evolution Level")
st.plotly_chart(fig)

# 💬 Query Box
st.markdown("### 💬 Ask any question")
st.info("Having any query related do ask here")
query = st.text_input("Type your question about this art form")

if query:
    with st.spinner("Answering with ChatGPT..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a smart bot helping with queries about {art_form} in {country}."},
                {"role": "user", "content": query}
            ]
        )
        answer = response.choices[0].message.content
        st.success(answer)

        tts_answer = gTTS(text=answer, lang='en')
        answer_fp = BytesIO()
        tts_answer.write_to_fp(answer_fp)
        st.audio(answer_fp.getvalue(), format='audio/mp3')

st.markdown("---")
st.caption("Built with ❤️ by Avika")
