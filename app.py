from dotenv import load_dotenv
import anthropic
import streamlit as st

load_dotenv()
client = anthropic.Anthropic()

st.title("AI Study Quiz")

with open ("notes.txt") as f:
    notes = f.read()

system_prompt = f"""You are a study quiz partner. Use only these notes:

{notes}

Ask ONE question at a time. After the student answers, say whether they're right,
briefly explain anything they missed, then ask the next question.
Keep replies short."""

def get_reply(messages):
    response = client.messages.create(
        model = "claude-haiku-5-5",
        max_tokens = 2000,
        system = system_prompt,
        messages = messages,
    )
    return "".join(block.text for block in response.content if block.type == "text")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "user", "content": "Start the quiz."}]
    reply = get_reply(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Show the chat history (skip the hidden "Start the quiz." message)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box
if answer := st.chat_input("Type your answer..."):
    st.session_state.messages.append({"role": "user", "content": answer})
    with st.chat_message("user"):
        st.markdown(answer)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_reply(st.session_state.messages)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})