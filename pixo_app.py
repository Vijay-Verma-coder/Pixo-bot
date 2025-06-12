import streamlit as st
import wikipedia
import requests
from PIL import Image
from io import BytesIO
from gtts import gTTS
import openai
from streamlit_extras.add_vertical_space import add_vertical_space

# 🧠 OpenAI key (replace with yours if needed)
openai.api_key = "sk-your-openai-key"  # ← put your real key here

# 🎨 Art forms
ART_FORMS = ["Dance", "Music", "Painting", "Sculpture", "Literature", "Architecture"]

# 🌍 Countries list including "World"
COUNTRIES = ["World", "India", "United States", "France", "Italy", "China", "Japan", "Brazil", "Egypt", "Greece"]  # (short list here, full list can be added)

# 📚 Wikipedia fetch
def get_wikipedia_data(art, country):
    topic = f"{art} in {country}" if country != "World" else art
    try:
        page = wikipedia.page(topic)
        summary = wikipedia.summary(topic, sentences=5)
        image = page.images[0] if page.images else None
        return summary, image
    except:
        return "Sorry, no information found.", None

# ✏️ AI simplify
def simplify_text(text):
    prompt = f"Explain this in a simple and friendly way for school students:\n{text}"
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content.strip()
    except:
        return "Couldn't simplify the content."

# 🔊 Text to speech
def speak_text(text):
    try:
        tts = gTTS(text)
        tts.save("speak.mp3")
        with open("speak.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    except:
        st.warning("Voice could not be generated.")

# 🤖 Query answerer
def answer_query(query, art, country):
    prompt = f"Answer in simple words: {query} related to {art} in {country}"
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content.strip()
    except:
        return "Sorry, I couldn't find the answer."

# 🌟 UI
st.set_page_config(page_title="Pixo Bot", layout="centered")
st.title("🎨 Pixo Bot - Art Revolution Explorer")

st.markdown("### Select an Art Form and Country to Explore:")
art = st.selectbox("🎭 Art Form", ART_FORMS)
country = st.selectbox("🌍 Country", COUNTRIES)

if st.button("🔍 Show Revolution"):
    with st.spinner("Fetching info..."):
        raw_text, image_url = get_wikipedia_data(art, country)
        simple = simplify_text(raw_text)

    st.subheader("📖 Art Revolution Summary")
    st.write(simple)

    if image_url:
        try:
            img_data = requests.get(image_url).content
            img = Image.open(BytesIO(img_data))
            st.image(img, caption=f"{art} in {country}", use_column_width=True)
        except:
            st.warning("Could not load image.")

    if st.button("🔊 Speak it"):
        speak_text(simple)

# 💬 Query area
add_vertical_space(2)
st.markdown("## ❓ Ask Anything")
st.info("Having any query related do ask here")
query = st.text_input("Type your question here...")

if query:
    with st.spinner("Answering..."):
        reply = answer_query(query, art, country)
        st.subheader("💬 Answer")
        st.write(reply)
