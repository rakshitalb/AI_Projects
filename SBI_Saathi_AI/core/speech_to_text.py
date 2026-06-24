"""
SBI Saathi AI – Speech to Text Module
Handles microphone capture and audio file transcription using SpeechRecognition.
"""

import speech_recognition as sr
from config.settings import (
    SPEECH_RECOGNITION_TIMEOUT,
    SPEECH_RECOGNITION_PHRASE_LIMIT,
    SPEECH_RECOGNITION_ENERGY_THRESHOLD,
)


class SpeechToText:
    """Wrapper around SpeechRecognition for capturing and transcribing speech."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = SPEECH_RECOGNITION_ENERGY_THRESHOLD

    def listen_from_microphone(self, language_code: str = "en-IN"):
        """
        Capture audio from the default microphone and transcribe it.

        Args:
            language_code (str): Language code for recognition (e.g., 'en-IN', 'hi-IN').

        Returns:
            dict: {"success": bool, "text": str, "error": str}
        """
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=SPEECH_RECOGNITION_TIMEOUT,
                    phrase_time_limit=SPEECH_RECOGNITION_PHRASE_LIMIT,
                )
            return self._transcribe(audio, language_code)

        except sr.WaitTimeoutError:
            return {"success": False, "text": "", "error": "No speech detected within timeout."}
        except OSError as e:
            return {"success": False, "text": "", "error": f"Microphone not accessible: {e}"}
        except Exception as e:
            return {"success": False, "text": "", "error": f"Unexpected error: {e}"}

    def transcribe_audio_file(self, file_path: str, language_code: str = "en-IN"):
        """
        Transcribe speech from an audio file (wav/aiff/flac).

        Args:
            file_path (str): Path to the audio file.
            language_code (str): Language code for recognition.

        Returns:
            dict: {"success": bool, "text": str, "error": str}
        """
        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
            return self._transcribe(audio, language_code)

        except FileNotFoundError:
            return {"success": False, "text": "", "error": f"Audio file not found: {file_path}"}
        except Exception as e:
            return {"success": False, "text": "", "error": f"Unexpected error: {e}"}

    def _transcribe(self, audio, language_code: str):
        """Internal helper to run Google's recognition engine on captured audio."""
        try:
            text = self.recognizer.recognize_google(audio, language=language_code)
            return {"success": True, "text": text, "error": ""}
        except sr.UnknownValueError:
            return {"success": False, "text": "", "error": "Could not understand audio."}
        except sr.RequestError as e:
            return {"success": False, "text": "", "error": f"Recognition service error: {e}"}