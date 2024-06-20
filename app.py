import os
import base64
import re
import json
import bcrypt
import streamlit as st
import openai
from openai import AssistantEventHandler
from dotenv import load_dotenv
import streamlit_authenticator as stauth

load_dotenv()

def str_to_bool(str_input):
    if not isinstance(str_input, str):
        return False
    return str_input.lower() == "true"

def verify_password(stored_password, provided_password):
    stored_password = stored_password.encode('utf-8')
    provided_password = provided_password.encode('utf-8')
    return bcrypt.checkpw(provided_password, stored_password)

def load_credentials():
    credentials = st.secrets["credentials"]["usernames"]
    return {
        user: {
            "name": details["name"],
            "hashed_password": details["password"],
        } for user, details in credentials.items()
    }

# Load environment variables
azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")
authentication_required = str_to_bool(os.environ.get("AUTHENTICATION_REQUIRED", False))
assistant_id = os.environ.get("ASSISTANT_ID")
assistant_title = os.environ.get("ASSISTANT_TITLE", "Assistants API UI")
enabled_file_upload_message = os.environ.get(
    "ENABLED_FILE_UPLOAD_MESSAGE", "Upload a file"
)

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

    def on_tool_call_created(self, tool_call):
        st.session_state.current_tool_input = ""
        with st.chat_message("Assistant"):
            st.session_state.current_tool_input_markdown = st.empty()

    def on_tool_call_delta(self, delta, snapshot):
        if 'current_tool_input_markdown' not in st.session_state:
            with st.chat_message("Assistant"):
                st.session_state.current_tool_input_markdown = st.empty()

        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                st.session_state.current_tool_input += delta.code_interpreter.input
                input_code = f"### code interpreter\ninput:\n```python\n{st.session_state.current_tool_input}\n```"
                st.session_state.current_tool_input_markdown.markdown(input_code, True)

            if delta.code_interpreter.outputs:
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        pass

    def on_tool_call_done(self, tool_call):
        if tool_call.type == "code_interpreter":
            input_code = f"### code interpreter\ninput:\n```python\n{tool_call.code_interpreter.input}\n```"
            st.session_state.current_tool_input_markdown.markdown(input_code, True)
            st.session_state.chat_log.append({"name": "assistant", "msg": input_code})
            st.session_state.current_tool_input_markdown = None
            for output in tool_call.code_interpreter.outputs:
                if output.type == "logs":
                    output = f"### code interpreter\noutput:\n```\n{output.logs}\n```"
                    with st.chat_message("Assistant"):
                        st.markdown(output, True)
                        st.session_state.chat_log.append(
                            {"name": "assistant", "msg": output}
                        )

if authentication_required and "credentials" in st.secrets:
    users = load_credentials()
    authenticator = stauth.Authenticate(
        username=list(users.keys()),
        password=[user["hashed_password"] for user in users.values
