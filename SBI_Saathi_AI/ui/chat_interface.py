"""
SBI Saathi AI – Chat Interface Module
Handles rendering of chat message history and the overall conversation panel,
using Streamlit's native chat elements.
"""

import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE


# ----------------------------
# Chat History Rendering
# ----------------------------
def render_chat_history(chat_history: list):
    """
    Render the full chat history using Streamlit's chat_message component.

    Args:
        chat_history (list): List of dicts, each like {"role": "user"/"assistant", "text": str}.
    """
    for msg in chat_history:
        role = msg.get("role", "assistant")
        text = msg.get("text", "")

        # Defensive normalization in case role is anything unexpected
        if role not in ("user", "assistant"):
            role = "assistant"

        avatar = "🧑" if role == "user" else "🏦"

        with st.chat_message(role, avatar=avatar):
            st.write(text)


def render_single_message(role: str, text: str):
    """
    Render a single chat message immediately (useful for streaming-style updates
    before a full st.rerun() takes place).

    Args:
        role (str): "user" or "assistant".
        text (str): Message content.
    """
    role = role if role in ("user", "assistant") else "assistant"
    avatar = "🧑" if role == "user" else "🏦"

    with st.chat_message(role, avatar=avatar):
        st.write(text)


# ----------------------------
# Conversation Panel (Header + History)
# ----------------------------
def render_conversation_panel(chat_history: list, show_header: bool = True):
    """
    Render the full conversation panel: optional header, then chat history.

    Args:
        chat_history (list): List of chat message dicts.
        show_header (bool): Whether to display the app title/tagline above the chat.
    """
    if show_header:
        st.title(f"🏦 {APP_NAME}")
        st.caption(APP_TAGLINE)
        st.divider()

    if not chat_history:
        st.info("👋 Start a conversation by typing a message or tapping 🎙️ Speak.")
        return

    render_chat_history(chat_history)


# ----------------------------
# Empty State Helper
# ----------------------------
def render_empty_state(message: str = "👋 Start a conversation by typing a message or tapping 🎙️ Speak."):
    """Render a friendly empty-state message when there is no chat history yet."""
    st.info(message)