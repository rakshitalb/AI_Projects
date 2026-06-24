"""
SBI Saathi AI – Intent Detection Module
Lightweight rule/keyword-based intent classifier for banking queries.
(Can be swapped later for an ML/LLM-based classifier without changing the interface.)
"""

import re

# ----------------------------
# Intent Definitions
# ----------------------------
INTENT_KEYWORDS = {
    "check_balance": [
        "balance", "how much money", "available balance", "account balance", "my balance"
    ],
    "fund_transfer": [
        "transfer", "send money", "pay", "send rs", "send ₹", "transfer money", "neft", "imps", "upi"
    ],
    "mini_statement": [
        "statement", "mini statement", "transaction history", "recent transactions", "last transactions"
    ],
    "card_block": [
        "block card", "block my card", "lost card", "stolen card", "deactivate card"
    ],
    "branch_locator": [
        "branch", "nearest branch", "atm", "nearest atm", "branch location"
    ],
    "interest_rates": [
        "interest rate", "fd rate", "fixed deposit rate", "loan rate", "rd rate"
    ],
    "loan_inquiry": [
        "loan", "apply for loan", "home loan", "personal loan", "car loan", "loan eligibility"
    ],
    "greeting": [
        "hi", "hello", "hey", "namaste", "good morning", "good evening"
    ],
    "help": [
        "help", "what can you do", "options", "menu", "assist"
    ],
}

# Simple entity patterns (amount, account number placeholders)
AMOUNT_PATTERN = re.compile(r"(?:rs\.?|₹|inr)\s?(\d+(?:,\d{3})*(?:\.\d+)?)", re.IGNORECASE)
ACCOUNT_PATTERN = re.compile(r"\b(\d{9,18})\b")


def detect_intent(text: str) -> dict:
    """
    Detect the most likely banking intent from English input text.

    Args:
        text (str): English text (already translated upstream if needed).

    Returns:
        dict: {
            "intent": str,          # matched intent key or "unknown"
            "confidence": float,    # naive confidence score
            "entities": dict,       # extracted entities (amount, account_number)
        }
    """
    if not text or not text.strip():
        return {"intent": "unknown", "confidence": 0.0, "entities": {}}

    normalized_text = text.lower().strip()

    best_intent = "unknown"
    best_score = 0

    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in normalized_text)
        if score > best_score:
            best_score = score
            best_intent = intent

    confidence = min(1.0, best_score / 2) if best_score > 0 else 0.0

    entities = _extract_entities(normalized_text)

    return {
        "intent": best_intent if best_score > 0 else "unknown",
        "confidence": confidence,
        "entities": entities,
    }


def _extract_entities(text: str) -> dict:
    """Extract simple entities like amount and account number from text."""
    entities = {}

    amount_match = AMOUNT_PATTERN.search(text)
    if amount_match:
        entities["amount"] = amount_match.group(1).replace(",", "")

    account_match = ACCOUNT_PATTERN.search(text)
    if account_match:
        entities["account_number"] = account_match.group(1)

    return entities