# gpt-assistants-api-ui

* 💬 SUI Memo Assistants chat UI
* 🛠️ Create an OpenAI Assistant and get the ASSISTANT ID
* 🏃 Supports Streaming API to ask quesitons for retrieval


## 🌟 Quick Start

1. 👤 Create an assistant on the OpenAI site & Get assistant ID (https://platform.openai.com/assistants)
2. 🔑 Get the API key from OpenAI (https://platform.openai.com/api-keys)
3. ⬇️ Clone the repository

    ```bash
    $ git clone https://github.com/ryo-ma/gpt-assistants-api-ui.git
    ```

4. 📦 Install dependencies

    ```bash
    $ poetry install
    ```

5. 🔑 Set environment variables

    ```bash
    OPENAI_API_KEY="sk-xxx"
    ASSISTANT_ID="asst_xxx"

    ASSISTANT_TITLE="Assistants API UI"
    ENABLED_FILE_UPLOAD_MESSAGE="Upload a file" # Leave empty to disable
   
    AUTHENTICATION_REQUIRED="False" # Must change to True if you require authentication
    ```
    If you use azure instead, set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_KEY`

6. 🔑 Set Authentication configuration (optional)

   To set up authentication, create a [secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) file `.streamlit/secrets.toml`  as below:

   ```toml
   [credentials]
   usernames = { jsmith = {failed_login_attempts = 0,  logged_in = false, name = "John Smith", password = "abc"}, rbriggs = {failed_login_attempts = 0,  logged_in = false, name = "R Briggs", password = "abc"}}
   
   [cookie]
   expiry_days = 30
   key = "some_signature_key"  # Must be string
   name = "some_cookie_name"
   ```
   Reference:  [Deploying Streamlit-Authenticator via Streamlit Community Cloud](https://discuss.streamlit.io/t/deploying-streamlit-authenticator-via-streamlit-community-cloud/39085)

7. 🏃‍️ Run the app

    ```bash
    $ poetry shell
    $ streamlit run app.py
    ```

## 🌐 Deploy to Streamlit Cloud
You can fork this repository and deploy the app to https://share.streamlit.io/. No need to run the app on your local machine.

> Don't forget to choose 3.10 as the Python version and set environment variables in the "Advanced settings" during deployment.

To use authentication with Streamlit Cloud, please use this TOML format:

```toml
# Environment variables
OPENAI_API_KEY="sk-xxx"
ASSISTANT_ID="asst_xxx"

ASSISTANT_TITLE="Assistants API UI"
ENABLED_FILE_UPLOAD_MESSAGE="Upload a file" # Leave empty to disable

AUTHENTICATION_REQUIRED="True"

# Authentication secrets
[credentials]
usernames = { jsmith = {failed_login_attempts = 0,  logged_in = false, name = "John Smith", password = "abc"}, rbriggs = {failed_login_attempts = 0,  logged_in = false, name = "R Briggs", password = "abc"}}

[cookie]
expiry_days = 30
key = "some_signature_key"  # Must be string
name = "some_cookie_name"
```
