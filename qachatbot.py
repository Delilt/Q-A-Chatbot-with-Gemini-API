from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


##funtion to load gemini 

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

#initialize the streamlit app

st.set_page_config(page_title="Q&A Chatbot")
st.header("Gemini LLM Application")

# initialize session state for chat history if it doesnt exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


input_text = st.text_input("input your prompt:", key = "input_text")
submit_button = st.button("get answer")

if submit_button and input_text:
    response = get_gemini_response(input_text)
    ## add user query and response to session chat history
    st.session_state['chat_history'].append(("you",input_text))
    st.subheader("the response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("bot",chunk.text))

st.subheader("the chat history is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role} : {text}")
