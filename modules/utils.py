
user_mode = {}

def is_human_mode(user_id):
    return user_mode.get(user_id, False)

def switch_mode(user_id, is_human):
    user_mode[user_id] = is_human

def save_message(user_id, message):
    print(f"[LOG] Save user ({user_id}): {message}")
