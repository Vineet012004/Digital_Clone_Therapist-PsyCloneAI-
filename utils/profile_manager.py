import json
import os
from pathlib import Path
from dotenv import load_dotenv


class ProfileManager:
    def __init__(self, profile_dir: str = "data/user_profiles"):
        self.profile_dir = Path(profile_dir)
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        load_dotenv()  # Load .env variables

    def load_user_profile(self, username: str) -> dict:
        """Load or create user profile"""
        profile_path = self.profile_dir / f"{username.lower()}.json"

        if profile_path.exists():
            with open(profile_path, "r") as f:
                profile = json.load(f)
        else:
            profile = {
                "name": username,
                "traits": {"communication_style": "neutral", "emotional_patterns": []},
                "metadata": {
                    "api_key_source": "global",
                },
                "llm_preferences": {
                    "model": "llama3-70b-8192",
                    "temperature": 0.7,
                    "max_tokens": 1024,
                },
            }
            self._save_profile(username, profile)

        return profile

    def _save_profile(self, username: str, data: dict):
        """Save profile to disk"""
        with open(self.profile_dir / f"{username.lower()}.json", "w") as f:
            json.dump(data, f, indent=2)

    def update_llm_preferences(
        self, username: str, model: str, temperature: float, max_tokens: int
    ):
        """Update LLM preferences for the user"""
        profile = self.load_user_profile(username)
        profile["llm_preferences"]["model"] = model
        profile["llm_preferences"]["temperature"] = temperature
        profile["llm_preferences"]["max_tokens"] = max_tokens
        self._save_profile(username, profile)
