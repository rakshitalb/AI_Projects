"""
SBI Saathi AI – Text to Speech Module
Converts text responses into speech audio using gTTS.
"""

import os
import uuid
from gtts import gTTS
from config.settings import AUDIO_DIR, TTS_DEFAULT_LANG, TTS_SLOW, TTS_OUTPUT_FORMAT


class TextToSpeech:
    """Wrapper around gTTS for generating speech audio files from text."""

    def __init__(self):
        self.output_dir = AUDIO_DIR

    def synthesize(self, text: str, language_code: str = TTS_DEFAULT_LANG, slow: bool = TTS_SLOW):
        """
        Convert given text into an audio file.

        Args:
            text (str): Text to convert to speech.
            language_code (str): Target language code (e.g., 'en', 'hi', 'kn').
            slow (bool): Whether to speak slowly.

        Returns:
            dict: {"success": bool, "file_path": str, "error": str}
        """
        if not text or not text.strip():
            return {"success": False, "file_path": "", "error": "Empty text provided."}

        try:
            filename = f"tts_{uuid.uuid4().hex}.{TTS_OUTPUT_FORMAT}"
            file_path = os.path.join(self.output_dir, filename)

            tts = gTTS(text=text, lang=language_code, slow=slow)
            tts.save(file_path)

            return {"success": True, "file_path": file_path, "error": ""}

        except ValueError as e:
            return {"success": False, "file_path": "", "error": f"Unsupported language code: {e}"}
        except Exception as e:
            return {"success": False, "file_path": "", "error": f"TTS generation failed: {e}"}

    def cleanup_audio_file(self, file_path: str):
        """Delete a generated audio file after playback to keep assets/audio clean."""
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception:
            pass
        return False