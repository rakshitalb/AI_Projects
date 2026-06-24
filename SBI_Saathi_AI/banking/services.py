"""
SBI Saathi AI – Banking Services Module
Mock/demo banking operations. Replace with real core-banking API calls in production.
"""

import json
import os
from config.settings import MOCK_USER_DATA_FILE, CURRENCY_SYMBOL

# ----------------------------
# Demo / Mock Data Loading
# ----------------------------
_DEFAULT_DEMO_USER = {
    "name": "Demo User",
    "account_number": "1234567890",
    "balance": 52340.75,
    "transactions": [
        {"date": "2025-06-01", "type": "credit", "amount": 5000, "description": "Salary credit"},
        {"date": "2025-06-03", "type": "debit", "amount": 1200, "description": "Electricity bill"},
        {"date": "2025-06-05", "type": "debit", "amount": 800, "description": "Grocery store"},
    ],
}


def _load_demo_user() -> dict:
    """Load mock user data from JSON file, falling back to a default demo profile."""
    try:
        if os.path.exists(MOCK_USER_DATA_FILE):
            with open(MOCK_USER_DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    return data[0]
                if isinstance(data, dict):
                    return data
    except Exception:
        pass
    return _DEFAULT_DEMO_USER


# ----------------------------
# Intent Handlers
# ----------------------------
def handle_intent(intent: str, text: str, entities: dict) -> dict:
    """
    Execute the banking action corresponding to a detected intent.

    Args:
        intent (str): Detected intent key.
        text (str): Original English text (for context, currently unused in mocks).
        entities (dict): Extracted entities like amount, account_number.

    Returns:
        dict: {"response_text": str}
    """
    handler = _INTENT_HANDLERS.get(intent, _handle_unknown)
    return handler(entities)


def _handle_check_balance(entities: dict) -> dict:
    user = _load_demo_user()
    balance = user.get("balance", 0)
    response = (
        f"Your available balance is {CURRENCY_SYMBOL}{balance:,.2f} "
        f"in account ending {str(user.get('account_number', ''))[-4:]}."
    )
    return {"response_text": response}


def _handle_fund_transfer(entities: dict) -> dict:
    amount = entities.get("amount")
    account_number = entities.get("account_number")

    if amount and account_number:
        response = (
            f"Sure, I can help transfer {CURRENCY_SYMBOL}{amount} to account "
            f"ending {account_number[-4:]}. Please confirm to proceed. "
            f"(Demo mode: no real transaction will occur.)"
        )
    elif amount:
        response = (
            f"You want to transfer {CURRENCY_SYMBOL}{amount}. "
            f"Please provide the recipient's account number to continue."
        )
    else:
        response = "Please tell me the amount and recipient account number for the transfer."

    return {"response_text": response}


def _handle_mini_statement(entities: dict) -> dict:
    user = _load_demo_user()
    transactions = user.get("transactions", [])

    if not transactions:
        return {"response_text": "No recent transactions found."}

    lines = []
    for txn in transactions[-5:]:
        sign = "+" if txn.get("type") == "credit" else "-"
        lines.append(
            f"{txn.get('date', '')}: {sign}{CURRENCY_SYMBOL}{txn.get('amount', 0)} - {txn.get('description', '')}"
        )

    response = "Here are your recent transactions: " + "; ".join(lines)
    return {"response_text": response}


def _handle_card_block(entities: dict) -> dict:
    response = (
        "I understand you want to block your card. For security, please call our 24x7 helpline "
        "at 1800-XXX-XXXX immediately, or confirm here to proceed with blocking in demo mode."
    )
    return {"response_text": response}


def _handle_branch_locator(entities: dict) -> dict:
    response = (
        "Please share your city or pin code, and I will find the nearest SBI branch or ATM for you."
    )
    return {"response_text": response}


def _handle_interest_rates(entities: dict) -> dict:
    response = (
        "Current indicative rates: Savings Account - 2.70% p.a., "
        "Fixed Deposit (1 year) - 6.80% p.a., Personal Loan starting from 10.90% p.a. "
        "Rates are subject to change; please check the official SBI website for the latest rates."
    )
    return {"response_text": response}


def _handle_loan_inquiry(entities: dict) -> dict:
    response = (
        "We offer Home, Personal, Car, and Education loans. "
        "Would you like to check your eligibility or learn more about a specific loan type?"
    )
    return {"response_text": response}


def _handle_greeting(entities: dict) -> dict:
    response = (
        "Hello! I am SBI Saathi, your banking companion. "
        "I can help you check balance, transfer funds, view mini statements, and more. How can I assist you today?"
    )
    return {"response_text": response}


def _handle_help(entities: dict) -> dict:
    response = (
        "I can help you with: checking account balance, fund transfer, mini statement, "
        "blocking a lost card, finding nearby branches/ATMs, interest rates, and loan inquiries. "
        "Just ask me in your own words!"
    )
    return {"response_text": response}


def _handle_unknown(entities: dict) -> dict:
    response = (
        "I'm sorry, I didn't quite understand that. You can ask me about balance, fund transfer, "
        "mini statement, card block, branch locator, interest rates, or loans."
    )
    return {"response_text": response}


# ----------------------------
# Intent -> Handler Mapping
# ----------------------------
_INTENT_HANDLERS = {
    "check_balance": _handle_check_balance,
    "fund_transfer": _handle_fund_transfer,
    "mini_statement": _handle_mini_statement,
    "card_block": _handle_card_block,
    "branch_locator": _handle_branch_locator,
    "interest_rates": _handle_interest_rates,
    "loan_inquiry": _handle_loan_inquiry,
    "greeting": _handle_greeting,
    "help": _handle_help,
    "unknown": _handle_unknown,
}