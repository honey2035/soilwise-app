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

# ---------- TITLE ----------
st.markdown(f"## {tr('🧪🌍 SoilWise: Detect, Grow, Thrive')}")

# ---------- INTRO ----------
st.markdown(f"### {tr('Welcome to SoilWise: Detect, Grow, Thrive! This app helps you grow better with soil-specific guidance.')}")

# ---------- USER TYPE ----------
st.markdown(f"### 👩🌾 {tr('Who are you?')}")
user_type = st.radio(tr("Choose your role:"), [tr("Farmer"), tr("Home Gardener")])
st.success(f"🌾 {tr('Professional Recommendations Mode Activated')} – {user_type}")

# -------------------- Voice Assistant --------------------
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

# ---------- IMAGE UPLOAD ----------
st.markdown(f"#### {tr('📷 Upload an image of your compost, plant, or food sample')}")
uploaded_file = st.file_uploader(tr("Limit 200MB per file • JPG, PNG, JPEG"), type=["jpg", "png", "jpeg"])
if uploaded_file:
    st.image(uploaded_file, caption=tr("Uploaded Image"), use_column_width=True)

# -------------------- Smart Crop & Soil Assistant --------------------
st.markdown(f"### {tr('🧬 Smart Crop & Soil Assistant')}")

crops = ["Tomato", "Potato", "Brinjal", "Chili", "Spinach"]
soils = ["Sandy", "Loamy", "Clay", "Red Soil", "Black Soil"]
composts = ["Cow dung mix", "Vermicompost", "Kitchen waste", "Dry leaves", "Banana peels"]

# Translate dropdown options
crop = st.selectbox(tr("Select a crop type:"), [tr(c) for c in crops])
soil = st.selectbox(tr("Select your soil type:"), [tr(s) for s in soils])
selected_composts = st.multiselect(tr("Select compost type(s):"), [tr(c) for c in composts])

# -------------------- Results --------------------
if crop and soil and selected_composts:
    st.markdown(f"### {tr('🧪 Estimated Soil Nutrients & Suggestions')}")

    st.write(f"**{tr('Crop')}:** {crop}")
    st.write(f"**{tr('Soil')}:** {soil}")
    st.write(f"**{tr('Compost(s)')}:** {', '.join(selected_composts)}")

    estimate = {
        "Nitrogen": "Moderate",
        "Phosphorus": "Low",
        "Potassium": "High",
        "pH": "6.5 (Slightly acidic)",
        "Organic Matter": "Good"
    }
    for key, val in estimate.items():
        st.write(f"**{tr(key)}:** {tr(val)}")

    st.markdown("#### 🌱 " + tr("AI Suggestions"))
    st.markdown(f"✅ {tr('Add bone meal for Phosphorus improvement')}")
    st.markdown(f"✅ {tr('Add neem cake powder for organic pest control')}")
    st.markdown(f"💧 {tr('Watering required:')} {tr('Twice a day during summer; once during winter')}")

# 🎙️ --- Voice Assistant Button UI (Dummy) ---
st.markdown("### 🎙️ Voice Assistant (Beta)")
st.markdown("Click the mic and speak — voice feature coming soon!")

mic_button = """
<div style="display:flex; align-items:center; gap:10px; margin-top:10px;">
    <button style="
        background-color:#4CAF50;
        color:white;
        border:none;
        padding:12px;
        font-size:16px;
        border-radius:50%;
        cursor: not-allowed;
    " disabled>
        🎤
    </button>
    <span style="font-size:16px; color:#555;">Listening temporarily disabled</span>
</div>
"""
st.markdown(mic_button, unsafe_allow_html=True)


# 🌱 --- Smart Suggestion Card (Dummy Logic) ---
st.markdown("### 🌿 Smart Crop & Soil Suggestion")

# Example dummy suggestion (you can later link this with your real inputs)
selected_crop = st.session_state.get("crop_type", "Potato")
soil_type = st.session_state.get("soil_type", "Clay")
compost = st.session_state.get("compost_type", "Kitchen waste")

# Dummy logic for advice (replace with real AI rules later)
suggestion = ""
if selected_crop == "Potato" and soil_type == "Clay":
    suggestion = "Add 2 liters of water every 3 days and mix dry leaves in your compost for better aeration."
elif selected_crop == "Tomato":
    suggestion = "Maintain moist soil. Add banana peel compost for potassium boost."
else:
    suggestion = "Use well-drained compost and water moderately every 2 days."

with st.container():
    st.markdown(f"""
    <div style="
        background-color: #e8f5e9;
        border-left: 6px solid #4CAF50;
        padding: 10px 20px;
        border-radius: 5px;
        margin-top: 10px;
    ">
        <h4 style="color:#2e7d32;">🌾 Suggestion for {selected_crop}</h4>
        <p style="color:#444;">{suggestion}</p>
    </div>
    """, unsafe_allow_html=True)
# -------------------- Footer --------------------
st.markdown("---")
st.caption(tr("SoilWise © 2025 - Developed for farmers and garden lovers 🌾"))
import streamlit as st
from streamlit.components.v1 import html
