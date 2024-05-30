import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

st.header("Amazon e-Ticaret Rehberiniz")
st.text("E-Ticaret hakkinda merak ettiklerinizi sorabilirsiniz.")

# Initialize the chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Bana e-ticaret hakkinda birşeyler sorabilirsiniz."}
    ]

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            # Initialize the chat message
            messages = [{"role": "user", "content": st.session_state.messages[-1]["content"]}]
            
            # Generate completions from the GPT-3.5-turbo model
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )
            
            # Display the response
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    st.write(chunk.choices[0].delta.content)
                    message = {"role": "assistant", "content": chunk.choices[0].delta.content}
                    st.session_state.messages.append(message)  # Add response to message history
                    break  # Stop processing further chunks
