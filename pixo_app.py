import streamlit as st
import wikipedia
import requests
from PIL import Image
import pyttsx3
from io import BytesIO
from streamlit_extras.let_it_rain import rain
from streamlit_extras.add_vertical_space import add_vertical_space

# -------- AI REWRITER (Simple logic) --------
def simplify_text(text):
    sentences = text.split('. ')
    simple_sentences = [s for s in sentences if 5 < len(s.split()) < 25]
    return '. '.join(simple_sentences[:5]) + "."

# -------- TEXT TO SPEECH --------
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --------- UI STARTS HERE ---------
st.set_page_config(page_title="Pixo - Art Revolution Bot", layout="centered")

# Animation + Greeting
st.image("https://media.giphy.com/media/BXrwTdoho6hkQ/giphy.gif", caption="Hi, I'm Pixo 🤖", use_column_width=True)
st.markdown("## 🎨 Welcome to **Pixo** – Let’s learn about our fantastic art forms!")
rain(emoji="✨", font_size=25, falling_speed=3, animation_length="infinite")

# Dropdown Options
art_forms = ["Dance", "Music", "Painting", "Architecture", "Literature", "Sculpture"]

countries = [
    "World", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad",
    "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the",
    "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini",
    "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada",
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia",
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
    "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho",
    "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives",
    "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco",
    "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau",
    "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania",
    "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa",
    "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone",
    "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain",
    "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania",
    "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda",
    "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu",
    "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

# Select Inputs
art = st.selectbox("🎭 Choose an art form", art_forms)
country = st.selectbox("🌍 Choose a country", countries)

# After selection
if art and country:
    topic = f"{art} revolution in {country}" if country != "World" else f"{art} revolution around the world"
    try:
        summary = wikipedia.summary(topic, sentences=10)
        page = wikipedia.page(topic)
        image_url = None
        for img in page.images:
            if img.endswith(('.jpg', '.png', '.jpeg')) and 'flag' not in img.lower():
                image_url = img
                break

        # Simplify content
        simplified = simplify_text(summary)

        st.subheader(f"🎨 {art} Revolution in {country}")
        st.write(simplified)

        if image_url:
            img = Image.open(requests.get(image_url, stream=True).raw)
            st.image(img, caption=f"{art} in {country}", use_column_width=True)

        if st.button("🔊 Speak Summary"):
            speak(simplified)

        add_vertical_space(2)

        # Query Feature
        st.markdown("### 💬 Having any query related do ask here")
        query = st.text_input("Ask your question about art revolution")

        if query:
            if all(word in query.lower() for word in ["art", "revolution"]):
                try:
                    q_summary = wikipedia.summary(query, sentences=5)
                    short_ans = simplify_text(q_summary)
                    st.success(short_ans)
                    if st.button("🔊 Speak Answer"):
                        speak(short_ans)
                except:
                    st.warning("Couldn't fetch an answer. Try rephrasing your query.")
            else:
                st.error("Please ask only about the revolution of art forms 🎭")

    except:
        st.warning("Couldn't find proper data. Try a different combination.")
