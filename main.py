import streamlit as st
from utils.llm_integration import DigitalCloneAI
from utils.profile_manager import ProfileManager
from utils.session_utils import save_conversation, load_conversation_history
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Digital Clone Therapist", page_icon="🧠", layout="centered"
)

# Initialize components
profile_manager = ProfileManager()
ai_instance = DigitalCloneAI(api_key=os.getenv("GROQ_API_KEY"))

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "ai" not in st.session_state:
    st.session_state.ai = ai_instance
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {"name": "", "traits": {}}
if "personality" not in st.session_state:
    st.session_state.personality = {
        "communication": "",
        "stress_response": "",
        "response_style": "",
        "convo_priority": "",
    }

# Sidebar
with st.sidebar:
    st.title("Personal Setup")
    user_name = st.text_input("Your Full Name", key="user_name")

    with st.form("personality_form"):
        st.header("Personality Profile")
        st.session_state.personality["communication"] = st.selectbox(
            "Communication Style",
            ["Select", "Thoughtful", "Direct", "Casual", "Formal"],
        )
        st.session_state.personality["stress_response"] = st.selectbox(
            "When stressed, you typically feel:",
            ["Select", "Anxious", "Frustrated", "Withdrawn", "Overwhelmed"],
        )
        st.session_state.personality["response_style"] = st.selectbox(
            "Your responses are usually:",
            ["Select", "Detailed", "Concise", "Logical", "Emotional"],
        )
        st.session_state.personality["convo_priority"] = st.selectbox(
            "What's most important in conversations?",
            ["Select", "Solutions", "Empathy", "Honesty", "Quick answers"],
        )

        if st.form_submit_button("Save Profile"):
            st.session_state.user_profile = {
                "name": user_name,
                "traits": st.session_state.personality,
            }
            st.success("Profile saved!")

    if st.button("Initialize Your Digital Clone"):
        if user_name and st.session_state.personality["communication"]:
            st.session_state.conversation = load_conversation_history(user_name)
            if not isinstance(st.session_state.conversation, list):
                st.session_state.conversation = []
            st.success(f"Welcome back, {user_name}!")
        else:
            st.warning("Please complete your profile first")

# Main Interface
st.title("Your Digital Clone Therapist")

# 🔽 Add image below the title
st.image("assets/therapist_banner.jpg", width="100", use_column_width=True)


st.markdown(
    """
<h4 style='color:#636EFA; font-weight:600;'>
See Yourself More Clearly Through AI Reflection 
</h4>
""",
    unsafe_allow_html=True,
)
st.caption(
    "For more Accuracy, let the assistant know some of your qualities in the sidebar ⬅️!"
)
st.markdown(
    "<style>div.stChatInput{padding-bottom: 2rem;}</style>", unsafe_allow_html=True
)

# Display conversation history
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input handling
if prompt := st.chat_input("What's on your mind today?"):
    st.session_state.conversation.append({"role": "user", "content": prompt})

    response = st.session_state.ai.generate_response(
        prompt=prompt,
        user_profile=st.session_state.user_profile,
        conversation_history=st.session_state.conversation[-6:],
    )

    st.session_state.conversation.append({"role": "assistant", "content": response})

    if st.session_state.user_profile.get("name"):
        save_conversation(
            st.session_state.user_profile["name"], st.session_state.conversation
        )

    st.rerun()

st.markdown("---")
st.caption("Developed by Vineet Sharma • vneetsharma01@gmail.com")
