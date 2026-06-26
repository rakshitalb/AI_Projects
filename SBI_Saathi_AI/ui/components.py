"""
SBI Saathi AI – Reusable UI Components
Low-level Streamlit widgets used to build the sidebar and input areas.
Kept independent of business logic (agent/banking) for clean separation of concerns.
"""

import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE


# ----------------------------
# Sidebar Components
# ----------------------------
def render_sidebar_header():
    """Render the app name and tagline at the top of the sidebar."""
    st.markdown(f"## 🏦 {APP_NAME}")
    st.caption(APP_TAGLINE)
    st.divider()


def render_language_selector(current_language: str = DEFAULT_LANGUAGE) -> str:
    """
    Render a language selection dropdown.

    Args:
        current_language (str): Currently selected language display name.

    Returns:
        str: The selected language display name (e.g., "English", "Hindi").
    """
    languages = list(SUPPORTED_LANGUAGES.keys())
    default_index = languages.index(current_language) if current_language in languages else 0

    selected_language = st.selectbox(
        "Choose your language / भाषा चुनें",
        options=languages,
        index=default_index,
        key="language_selector_widget",
    )
    return selected_language


def render_clear_button() -> bool:
    """
    Render a button to clear the conversation history.

    Returns:
        bool: True if the button was clicked this run, else False.
    """
    return st.button("🗑️ Clear Conversation", key="clear_conversation_button")


# ----------------------------
# Input Components
# ----------------------------
def render_voice_input_button() -> bool:
    """
    Render the microphone/voice input trigger button.

    Returns:
        bool: True if the button was clicked this run, else False.
    """
    return st.button("🎙️ Speak", key="voice_input_button")


def render_text_input(placeholder: str = "Type your message here...") -> str:
    """
    Render the chat text input box.

    Args:
        placeholder (str): Placeholder text shown in the input box.

    Returns:
        str | None: The submitted text, or None if nothing was submitted this run.
    """
    return st.chat_input(placeholder, key="text_input_widget")


# ----------------------------
# Audio Output Component
# ----------------------------
def render_audio_player(audio_file_path: str, autoplay: bool = True):
    """
    Render an audio player for a generated TTS response.

    Args:
        audio_file_path (str | None): Path to the audio file. If None/empty, nothing is rendered.
        autoplay (bool): Whether the audio should autoplay.
    """
    if audio_file_path:
        st.audio(audio_file_path, format="audio/mp3", autoplay=autoplay)