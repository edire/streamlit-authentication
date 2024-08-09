#%% Import Libraries

import os
import streamlit as st
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from time import sleep


#%% Google OAuth Functions

LOGIN_TITLE = os.getenv('LOGIN_TITLE', 'Mastermind Reporting')
CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILE')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:8501')


def _get_flow():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file = CLIENT_SECRETS_FILE,
        scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
        redirect_uri=REDIRECT_URI,
    )
    return flow


def login():
    flow = _get_flow()
    authorization_url, state = flow.authorization_url()
    html_content = f"""
<div style="display: flex; justify-content: "center";">
<a href="{authorization_url}" target="_self" style="background-color: '#4285f4'; color: '#fff'; text-decoration: none; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; padding: 8px 12px; border-radius: 4px; display: flex; align-items: center;">
<img src="https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA" alt="Google logo" style="margin-right: 8px; width: 26px; height: 26px; background-color: white; border: 2px solid white; border-radius: 4px;">
Sign in with Google
</a>
</div>
"""
    st.title(LOGIN_TITLE)
    st.markdown(html_content, unsafe_allow_html=True)
    

def callback():
    sleep(3)
    flow = _get_flow()
    auth_code = st.query_params.get("code")
    st.query_params.clear()
    flow.fetch_token(code=auth_code)
    credentials = flow.credentials
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    email = user_info.get('email')
    return email


#%%