import os
import base64
import re
import json
import bcrypt
import streamlit as st
import openai
from openai import AssistantEventHandler
from dotenv import load_dotenv

load_dotenv()

def str_to_bool(str_input):
    if not isinstance(str_input, str):
        return False
    return str_input.lower() == "true"

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def load_credentials():
    credentials = st.secrets["credentials"]["usernames"]
    return {
        user: {
            "name": details["name"],
            "hashed_password": details["password"].encode('utf-8')
        } for user, details in credentials.items()
    }

azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")
authentication_required = str_to_bool(os.environ.get("AUTHENTICATION_REQUIRED", False))
assistant_id = os.environ.get("ASSISTANT_ID")
assistant_title = os.environ.get("ASSISTANT_TITLE", "Assistants API UI")
enabled_file_upload_message = os.environ.get("ENABLED_FILE_UPLOAD_MESSAGE", "Upload a file")

client = None
if azure_openai_endpoint and azure_openai_key:
    client = openai.AzureOpenAI(
        api_key=azure_openai_key,
        api_version="2024-02-15-preview",
        azure_endpoint=azure_openai_endpoint,
    )
else:
    client = openai.OpenAI(api_key=openai_api_key)

class EventHandler(AssistantEventHandler):
    def on_event(self, event):
        pass

    def on_text_created(self, text):
        st.session_state.current_message = ""
        with st.chat_message("Assistant"):
            st.session_state.current_markdown = st.empty()

    def on_text_delta(self, delta, snapshot):
        if snapshot.value:
            text_value = re.sub(
                r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", "Download Link", snapshot.value
            )
            st.session_state.current_message = text_value
            st.session_state.current_markdown.markdown(
                st.session_state.current_message, True
            )

    def on_text_done(self, text):
        format_text = format_annotation(text)
        st.session_state.current_markdown.markdown(format_text, True)
        st.session_state.chat_log.append({"name": "assistant", "msg": format_text})

def main():
    st.title(assistant_title)

    if authentication_required:
        credentials = load_credentials()
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user_info = credentials.get(username)
            if user_info and verify_password(user_info["hashed_password"], password):
                st.session_state["authenticated"] = True
                st.sidebar.success("Login successful!")
            else:
                st.sidebar.error("Failed to authenticate.")
                return

    if not authentication_required or st.session_state.get("authenticated", False):
        user_msg = st.text
