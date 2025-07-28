import streamlit as st
from deep_translator import GoogleTranslator
from PIL import Image
import base64
import speech_recognition as sr

# ---------- BACKGROUND IMAGE SETUP ----------
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        img = img_file.read()
    b64_encoded = base64.b64encode(img).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{b64_encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("background.jpg")

# ---------- SIDEBAR MENU ----------
choice = st.sidebar.selectbox("🔍 Select Feature", [
    "Home",
    "🎙️ Voice Assistant"
])

# ---------- LANGUAGE SETUP ----------
language_labels = {
    "English": "english",
    "हिन्दी (Hindi)": "hindi",
    "తెలుగు (Telugu)": "telugu",
    "தமிழ் (Tamil)": "tamil",
    "ಕನ್ನಡ (Kannada)": "kannada"
}
lang = st.selectbox("🌐 Choose your language", list(language_labels.keys()))
lang_code = language_labels[lang]

def tr(text):
    try:
        if lang_code == 'english':
            return text
        return GoogleTranslator(source='en', target=lang_code).translate(text)
    except:
        return text

# ---------------------- MAIN PAGE ----------------------
if choice == "Home":
    st.markdown(f"## {tr('🧪🌍 SoilWise: Detect, Grow, Thrive')}")
    st.markdown(f"### {tr('Welcome to SoilWise: Detect, Grow, Thrive! This app helps you grow better with soil-specific guidance.')}")

    st.markdown(f"### 👩🌾 {tr('Who are you?')}")
    user_type = st.radio(tr("Choose your role:"), [tr("Farmer"), tr("Home Gardener")])
    st.success(f"🌾 {tr('Professional Recommendations Mode Activated')} – {user_type}")

    st.markdown(f"### {tr('🎙️ Voice Assistant')}")
    if st.button(tr("Start Voice Input")):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.info(tr("Listening... please speak"))
                audio = r.listen(source, timeout=5)
                voice_text = r.recognize_google(audio)
                st.success(f"{tr('You said:')} {voice_text}")
        except Exception as e:
            st.error(tr("Voice recognition failed. Please try again."))

    st.markdown(f"#### {tr('📷 Upload an image of your compost, plant, or food sample')}")
    uploaded_file = st.file_uploader(tr("Limit 200MB per file • JPG, PNG, JPEG"), type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption=tr("Uploaded Image"), use_column_width=True)

    st.markdown(f"### {tr('🧬 Smart Crop & Soil Assistant')}")

    # Single set of inputs
crop = st.selectbox("Select a crop type:", ["Tomato", "Potato", "Carrot", "Brinjal", "Spinach"])
soil_type = st.selectbox("Select your soil type:", ["Sandy", "Loamy", "Clayey", "Black"])
compost = st.multiselect("Select compost type(s):", ["Banana peels", "Vermicompost", "Cow dung", "Kitchen Waste", "Dry leaves"])
moisture = st.slider("Moisture Level", 0, 100, 50)
temperature = st.slider("Temperature (°C)", 0, 50, 25)

# Submit button
if st.button("🔍 Get AI Suggestion"):
    # Show user input summary
    st.subheader("🧪 Estimated Soil Nutrients & Suggestions")
    st.markdown(f"**Crop:** {crop}")
    st.markdown(f"**Soil:** {soil_type}")
    st.markdown(f"**Compost(s):** {', '.join(compost)}")
    st.markdown(f"**Moisture Level:** {moisture}%")
    st.markdown(f"**Temperature:** {temperature}°C")

    # Dummy nutrient estimation (can be AI-powered later)
    st.markdown("**Nitrogen:** Moderate")
    st.markdown("**Phosphorus:** Low")
    st.markdown("**Potassium:** High")
    st.markdown("**pH:** 6.5 (Slightly acidic)")
    st.markdown("**Organic Matter:** Good")

    # AI Suggestions based on input
    st.subheader("🌱 AI Suggestions")
    if "Banana peels" in compost:
        st.markdown("✅ Banana peels add potassium – good for flowering.")
    if "Vermicompost" in compost:
        st.markdown("✅ Vermicompost improves soil structure and microbial activity.")
    if "Cow dung" in compost:
        st.markdown("✅ Cow dung boosts nitrogen and promotes root growth.")
    if "Kitchen Waste" in compost:
        st.markdown("✅ Decomposed kitchen waste adds balanced nutrients.")
    if "Dry leaves" in compost:
        st.markdown("✅ Dry leaves improve aeration and organic matter.")

    if soil_type == "Sandy":
        st.markdown("✅ Sandy soil needs frequent watering and more organic matter.")
    elif soil_type == "Clayey":
        st.markdown("✅ Clayey soil retains moisture; avoid overwatering.")
    elif soil_type == "Loamy":
        st.markdown("✅ Loamy soil is ideal for most vegetables.")
    elif soil_type == "Black":
        st.markdown("✅ Black soil is rich in minerals, great for cotton and legumes.")

    st.markdown("💧 **Watering Tip:** Adjust frequency based on temperature and moisture level.")

# ---------------------- VOICE ASSISTANT PAGE ----------------------
elif choice == "🎙️ Voice Assistant":
    st.markdown("## 🎙️ Voice Assistant")
    st.write("Speak your query about soil, crop, or nutrients...")

    def recognize_speech_from_mic():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Speak now!")
            audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            st.success("Processing your voice...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Could not request results from Google Speech Recognition."

    if st.button("🎤 Start Listening"):
        user_voice = recognize_speech_from_mic()
        st.write(f"**You said:** _{user_voice}_")

        user_voice_lower = user_voice.lower()
        if "acidic" in user_voice_lower or "ph low" in user_voice_lower:
            st.markdown("### 🌱 AI Suggestion:")
            st.write("- Add lime (calcium carbonate) to increase pH.")
            st.write("- Grow crops like spinach, broccoli, or beets.")
        elif "dry" in user_voice_lower or "lack water" in user_voice_lower:
            st.markdown("### 💧 AI Suggestion:")
            st.write("- Use mulch to retain soil moisture.")
            st.write("- Consider drip irrigation.")
        elif "sandy" in user_voice_lower:
            st.markdown("### 🏜️ AI Suggestion:")
            st.write("- Mix organic matter (cow dung, compost) into soil.")
            st.write("- Grow crops like watermelon or carrots.")
        elif "fertilizer" in user_voice_lower:
            st.markdown("### 🌾 AI Suggestion:")
            st.write("- Use NPK 10:26:26 if your crop is in flowering stage.")
        else:
            st.markdown("### 🤖 AI Suggestion:")
            st.write("- Sorry, I couldn't find a match. Try asking about pH, fertilizer, or soil type.")

# -------------------- Footer --------------------
st.markdown("---")
st.caption(tr("SoilWise © 2025 - Developed for farmers and garden lovers 🌾"))
