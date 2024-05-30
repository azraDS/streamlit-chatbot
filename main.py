import streamlit as st
import openai

# Initialize OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.header("Amazon e-Ticaret Rehberiniz")
st.text("E-Ticaret hakkinda merak ettiklerinizi sorabilirsiniz.")

from PIL import Image


# Initialize the chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Bana e-ticaret hakkinda birşeyler sorabilirsiniz."}
    ]

# Function to generate a response from OpenAI GPT-3.5-turbo
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable e-commerce assistant. Your users are asking questions about products, orders, or e-commerce advice. Answer the user's question concisely. If you don't know the answer, just say you don't know. Answer the question in the language asked."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            response_content = generate_response(st.session_state.messages[-1]["content"])
            st.write(response_content)
            message = {"role": "assistant", "content": response_content}
            st.session_state.messages.append(message)  # Add response to message history
