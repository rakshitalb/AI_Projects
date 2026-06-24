"""
SBI Saathi AI – Core Agent Module
Orchestrates translation, intent detection, and banking logic to
generate a response to user queries, regardless of input language.
"""

from core.translator import Translator
from banking.intents import detect_intent
from banking.services import handle_intent
from config.settings import DEFAULT_LANGUAGE_CODE


class SaathiAgent:
    """
    The core agentic orchestrator for SBI Saathi AI.

    Flow:
        1. Translate user input (any language) -> English.
        2. Detect banking intent from English text.
        3. Execute the corresponding banking action/response.
        4. Translate the English response back to the user's language.
    """

    def __init__(self):
        self.translator = Translator()

    def process_query(self, user_text: str, user_lang_code: str = DEFAULT_LANGUAGE_CODE):
        """
        Process a user's query end-to-end and return a localized response.

        Args:
            user_text (str): Raw text from the user (in their chosen language).
            user_lang_code (str): Language code of the user's input/output (e.g., 'hi', 'kn').

        Returns:
            dict: {
                "success": bool,
                "response_text": str,        # final response in user's language
                "response_text_en": str,     # response in English (for logging/debug)
                "intent": str,
                "error": str,
            }
        """
        if not user_text or not user_text.strip():
            return {
                "success": False,
                "response_text": "",
                "response_text_en": "",
                "intent": "",
                "error": "Empty query provided.",
            }

        # Step 1: Translate input to English (skip if already English)
        if user_lang_code != "en":
            translation_result = self.translator.to_english(user_text)
            if not translation_result["success"]:
                return {
                    "success": False,
                    "response_text": "",
                    "response_text_en": "",
                    "intent": "",
                    "error": translation_result["error"],
                }
            english_text = translation_result["translated_text"]
        else:
            english_text = user_text

        # Step 2: Detect intent
        intent_result = detect_intent(english_text)
        intent = intent_result.get("intent", "unknown")

        # Step 3: Execute banking logic for the detected intent
        action_result = handle_intent(intent, english_text, intent_result.get("entities", {}))
        response_text_en = action_result.get("response_text", "Sorry, I could not process that request.")

        # Step 4: Translate response back to user's language
        if user_lang_code != "en":
            back_translation = self.translator.from_english(response_text_en, target_lang=user_lang_code)
            if back_translation["success"]:
                final_response = back_translation["translated_text"]
            else:
                # Fallback to English if back-translation fails
                final_response = response_text_en
        else:
            final_response = response_text_en

        return {
            "success": True,
            "response_text": final_response,
            "response_text_en": response_text_en,
            "intent": intent,
            "error": "",
        }