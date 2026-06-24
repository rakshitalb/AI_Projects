"""
SBI Saathi AI – Configuration Settings
Centralized constants, API keys, and language mappings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ----------------------------
# App Metadata
# ----------------------------
APP_NAME = "SBI Saathi AI"
APP_TAGLINE = "Agentic Banking Companion for Digital Adoption"
APP_VERSION = "0.1.0"

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
STYLES_DIR = os.path.join(ASSETS_DIR, "styles")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure runtime directories exist
os.makedirs(AUDIO_DIR, exist_ok=True)

# ----------------------------
# API Keys / Secrets
# ----------------------------
# Add any third-party API keys here if needed in future
# Example: OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ----------------------------
# Speech Recognition Settings
# ----------------------------
SPEECH_RECOGNITION_TIMEOUT = 5          # seconds to wait for phrase start
SPEECH_RECOGNITION_PHRASE_LIMIT = 15    # max seconds of recording
SPEECH_RECOGNITION_ENERGY_THRESHOLD = 300

# ----------------------------
# Text-to-Speech (gTTS) Settings
# ----------------------------
TTS_DEFAULT_LANG = "en"
TTS_SLOW = False
TTS_OUTPUT_FORMAT = "mp3"

# ----------------------------
# Supported Languages
# (Mapping: Display Name -> Language Code)
# ----------------------------
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Malayalam": "ml",
    "Odia": "or",
    "Urdu": "ur",
}

DEFAULT_LANGUAGE = "English"
DEFAULT_LANGUAGE_CODE = "en"

# ----------------------------
# Google Translate Settings
# ----------------------------
TRANSLATE_SOURCE_AUTO = "auto"

# ----------------------------
# Banking Demo Settings
# ----------------------------
MOCK_USER_DATA_FILE = os.path.join(DATA_DIR, "sample_users.json")
CURRENCY_SYMBOL = "₹"

# ----------------------------
# Logging
# ----------------------------
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"