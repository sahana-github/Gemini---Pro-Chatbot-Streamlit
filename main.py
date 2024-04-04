import os
import streamlit as st
from dotenv import load_dotenv
from google import generativeai as gen_ai
#load environment variables
load_dotenv()

#configure streamlit variables
st.set_page_config(
    page_title="Chat with Gemini-Pro",
    page_icon=":brain:", #Favicon emoji
    layout="centered", #page layout option
)

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

#set up goggle gemini-pro Ai model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model=gen_ai.GenerativeModel('gemini-pro')

#function to translate roles between Gemini-Pro and Streamlit terminology 1 usage
def translate_role_for_streamlit(user_role):
    if user_role=="model":
        return "assistant"
    else:
        return user_role

#initialize chat session in streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session=model.start_chat(history=[])

#display the chatbots title on the page
st.title(" Gemini Pro - ChatBot")

#display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

#Input feild for users message
user_prompt=st.chat_input("Ask Gemini-Pro....")
if user_prompt:
    #add users message to display it
    st.chat_message('user').markdown(user_prompt)

    #send users message to gemini-pro and get the response
    gemini_response=st.session_state.chat_session.send_message(user_prompt)

    #Display gemini-pro response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)