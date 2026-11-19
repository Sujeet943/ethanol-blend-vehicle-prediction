
# ==========================================================
# CONVERSATION MEMORY
# ==========================================================

conversation_history = []

MAX_HISTORY_MESSAGES = 10
MAX_MESSAGE_LENGTH = 1000


# ==========================================================
# ADD MESSAGE
# ==========================================================

def add_message(role, content):

    # Store only user questions in memory.
    # Do not store assistant-generated answers.
    if role.lower() != "user":
        return

    if not isinstance(content, str):
        return

    content = content.strip()

    if not content:
        return

    conversation_history.append({
        "role": "User",
        "content": content[:MAX_MESSAGE_LENGTH]
    })

    # Keep only the latest 10 user messages.
    while len(conversation_history) > MAX_HISTORY_MESSAGES:
        conversation_history.pop(0)


# ==========================================================
# GET HISTORY
# ==========================================================

def get_history():

    history = ""

    for msg in conversation_history:

        history += (
            f"{msg['role']}: {msg['content']}\n"
        )

    return history


# ==========================================================
# CLEAR HISTORY
# ==========================================================

def clear_history():

    conversation_history.clear()

    print("Conversation history cleared.")
