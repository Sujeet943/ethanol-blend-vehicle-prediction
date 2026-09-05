conversation_history = []


def add_message(role, content):
    conversation_history.append({
        "role": role,
        "content": content
    })


def get_history():

    history = ""

    for msg in conversation_history:
        history += f"{msg['role']}: {msg['content']}\n"

    return history


def clear_history():
    conversation_history.clear()