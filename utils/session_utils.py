import json
from pathlib import Path
from datetime import datetime


def save_conversation(username: str, conversation: list):
    try:
        history_dir = Path("data/conversation_history")
        history_dir.mkdir(exist_ok=True)

        filename = f"{username.lower()}_conversation.json"
        with open(history_dir / filename, "w") as f:
            json.dump(
                {
                    "user": username,
                    "last_updated": datetime.now().isoformat(),
                    "messages": conversation,
                },
                f,
                indent=2,
            )
    except Exception:
        pass  # Silent fail for demo purposes


def load_conversation_history(username: str) -> list:
    try:
        history_dir = Path("data/conversation_history")
        if not history_dir.exists():
            return []

        filename = f"{username.lower()}_conversation.json"
        if not (history_dir / filename).exists():
            return []

        with open(history_dir / filename, "r") as f:
            data = json.load(f)
            if isinstance(data.get("messages"), list):
                return data["messages"]
            return []
    except Exception:
        return []  # Return empty list if any error occurs
