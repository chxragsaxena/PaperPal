import streamlit as st
from utils.api import ask_question

def render_chat():
    st.set_page_config(page_title="JioGPT", layout="wide")
    st.markdown("<h2 style='margin-top: 3rem;'>💬 Chat with your documents</h2>", unsafe_allow_html=True)

    # Style for assistant message
    st.markdown("""
        <style>
            .assistant-msg {
                background-color: #2b3035 !important;
                color: white !important;
                padding: 12px 15px;
                border-radius: 10px;
                margin-bottom: 10px;
                line-height: 1.6;
            }
        </style>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render history
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.chat_message("user").markdown(content)
        else:
            st.markdown(f"<div class='assistant-msg'>{content['answer']}</div>", unsafe_allow_html=True)
            if content["sources"]:
                with st.expander("📄 View Sources"):
                    for src in content["sources"]:
                        st.markdown(f"- `{src}`")

    # Input + API call
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = ask_question(user_input)
        if response.status_code == 200:
            data = response.json()
            answer = data["response"]
            sources = data.get("sources", [])

            # Show styled message
            st.markdown(f"<div class='assistant-msg'>{answer}</div>", unsafe_allow_html=True)
            if sources:
                with st.expander("📄 View Sources"):
                    for src in sources:
                        st.markdown(f"- `{src}`")

            # Save in history with sources
            st.session_state.messages.append({
                "role": "assistant",
                "content": {
                    "answer": answer,
                    "sources": sources
                }
            })
        else:
            st.error(f"Error: {response.text}")
