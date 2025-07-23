from groq import Groq
from typing import Optional, List, Dict


class DigitalCloneAI:
    def __init__(self, api_key: str, model_name: str = "llama3-70b-8192"):
        self.model = model_name
        self.client = Groq(api_key=api_key)
        self.base_prompt = """You are a digital clone that mirrors the user's personality.
        Communication Style: {communication}
        Stress Response: {stress_response}
        Response Style: {response_style}
        Conversation Priority: {convo_priority}"""

    def generate_response(
        self,
        prompt: str,
        user_profile: Optional[Dict] = None,
        conversation_history: List[Dict] = None,
    ) -> str:
        try:
            messages = []

            # Add base prompt with personality traits
            traits = user_profile.get("traits", {}) if user_profile else {}
            messages.append(
                {
                    "role": "system",
                    "content": self.base_prompt.format(
                        communication=traits.get("communication", "neutral"),
                        stress_response=traits.get("stress_response", ""),
                        response_style=traits.get("response_style", ""),
                        convo_priority=traits.get("convo_priority", ""),
                    ),
                }
            )

            # Add conversation history
            if conversation_history:
                messages.extend(
                    [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in conversation_history
                        if "role" in msg and "content" in msg
                    ]
                )

            # Add current prompt
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.7, max_tokens=1024
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"Error: {str(e)}"
