"""
SBI Saathi AI – Main Streamlit Application
Agentic Banking Companion for Digital Adoption.
"""

import streamlit as st

from config.settings import (
    APP_NAME,
    APP_TAGLINE,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
)
from core.speech_to_text import SpeechToText
from core.text_to_speech import TextToSpeech
from core.agent import SaathiAgent

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏦",
    layout="centered",
)

# ----------------------------
# Initialize Core Modules (cached across reruns)
# ----------------------------
@st.cache_resource
def get_stt_engine():
    return SpeechToText()


@st.cache_resource
def get_tts_engine():
    return TextToSpeech()


@st.cache_resource
def get_agent():
    return SaathiAgent()


stt_engine = get_stt_engine()
tts_engine = get_tts_engine()
agent = get_agent()

# ----------------------------
# Session State Initialization
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"role": "user"/"assistant", "text": str}

if "selected_language" not in st.session_state:
    st.session_state.selected_language = DEFAULT_LANGUAGE

# ----------------------------
# Sidebar – Settings
# ----------------------------
with st.sidebar:
    st.markdown(f"## 🏦 {APP_NAME}")
    st.caption(APP_TAGLINE)
    st.divider()

    st.session_state.selected_language = st.selectbox(
        "Choose your language / भाषा चुनें",
        options=list(SUPPORTED_LANGUAGES.keys()),
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.selected_language),
    )

    st.divider()
    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()

# ----------------------------
# Main Header
# ----------------------------
st.title(f"🏦 {APP_NAME}")
st.caption(APP_TAGLINE)
st.divider()

# ----------------------------
# Chat History Display
# ----------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

# ----------------------------
# Input Section: Voice + Text
# ----------------------------
lang_code = SUPPORTED_LANGUAGES[st.session_state.selected_language]
stt_lang_code = f"{lang_code}-IN"  # SpeechRecognition expects locale format

col1, col2 = st.columns([1, 4])

with col1:
    voice_clicked = st.button("🎙️ Speak")

with col2:
    text_input = st.chat_input("Type your message here...")


# ----------------------------
# Shared Query Processing
# ----------------------------
def process_and_respond(user_text: str):
    """Run the agent on user_text, update chat history, and play TTS response."""
    st.session_state.chat_history.append({"role": "user", "text": user_text})

    with st.spinner("Thinking..."):
        agent_result = agent.process_query(user_text, user_lang_code=lang_code)

    if agent_result["success"]:
        response_text = agent_result["response_text"]
    else:
        response_text = f"⚠️ Sorry, something went wrong: {agent_result['error']}"

    st.session_state.chat_history.append({"role": "assistant", "text": response_text})

    tts_result = tts_engine.synthesize(response_text, language_code=lang_code)
    if tts_result["success"]:
        st.session_state["_last_audio_path"] = tts_result["file_path"]
    else:
        st.session_state["_last_audio_path"] = None


# ----------------------------
# Handle Voice Input
# ----------------------------
if voice_clicked:
    with st.spinner("Listening... please speak now"):
        result = stt_engine.listen_from_microphone(language_code=stt_lang_code)

    if result["success"]:
        process_and_respond(result["text"])
        st.rerun()
    else:
        st.error(f"⚠️ {result['error']}")

# ----------------------------
# Handle Text Input
# ----------------------------
if text_input:
    process_and_respond(text_input)
    st.rerun()

# ----------------------------
# Play Last Generated Audio (after rerun)
# ----------------------------
if st.session_state.get("_last_audio_path"):
    st.audio(st.session_state["_last_audio_path"], format="audio/mp3", autoplay=True)