"""
SBI Saathi AI – Translator Module
Handles language detection and translation using Google Translate (googletrans).
"""

from googletrans import Translator as GoogleTranslator
from config.settings import TRANSLATE_SOURCE_AUTO, DEFAULT_LANGUAGE_CODE


class Translator:
    """Wrapper around googletrans for detecting and translating text."""

    def __init__(self):
        self.engine = GoogleTranslator()

    def detect_language(self, text: str):
        """
        Detect the language of the given text.

        Args:
            text (str): Input text.

        Returns:
            dict: {"success": bool, "lang_code": str, "confidence": float, "error": str}
        """
        if not text or not text.strip():
            return {"success": False, "lang_code": "", "confidence": 0.0, "error": "Empty text provided."}

        try:
            detection = self.engine.detect(text)
            return {
                "success": True,
                "lang_code": detection.lang,
                "confidence": getattr(detection, "confidence", 0.0) or 0.0,
                "error": "",
            }
        except Exception as e:
            return {"success": False, "lang_code": "", "confidence": 0.0, "error": f"Detection failed: {e}"}

    def translate_text(self, text: str, target_lang: str, source_lang: str = TRANSLATE_SOURCE_AUTO):
        """
        Translate text into the target language.

        Args:
            text (str): Text to translate.
            target_lang (str): Target language code (e.g., 'en', 'hi', 'kn').
            source_lang (str): Source language code, defaults to auto-detect.

        Returns:
            dict: {"success": bool, "translated_text": str, "detected_source": str, "error": str}
        """
        if not text or not text.strip():
            return {"success": False, "translated_text": "", "detected_source": "", "error": "Empty text provided."}

        try:
            result = self.engine.translate(text, dest=target_lang, src=source_lang)
            return {
                "success": True,
                "translated_text": result.text,
                "detected_source": result.src,
                "error": "",
            }
        except Exception as e:
            return {"success": False, "translated_text": "", "detected_source": "", "error": f"Translation failed: {e}"}

    def to_english(self, text: str):
        """Convenience method: translate any input text to English."""
        return self.translate_text(text, target_lang="en")

    def from_english(self, text: str, target_lang: str = DEFAULT_LANGUAGE_CODE):
        """Convenience method: translate English text to a target language."""
        return self.translate_text(text, target_lang=target_lang, source_lang="en")