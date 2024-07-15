#%% Import Libraries

import os
import streamlit as st
from extra_streamlit_components import CookieManager
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import hashlib
import functools
from time import sleep
from cryptography.fernet import Fernet


#%% Miscellaneous Functions

def __set_session_var(name, var):
    sleep(1)
    st.session_state[name] = var


def __ensure_cookie(cookie_name, value=None):
    is_good = False
    cookie_value = st.session_state['cookie_manager'].get(cookie_name)
    if cookie_value == value:
        is_good = True
    return is_good


def __set_cookie(cookie_name, value, key):
    st.session_state['cookie_manager'].set(cookie_name, value, key, secure=True, same_site="None")


def __hasher(input_string, secret_string=os.getenv('SECRET_STRING')):
    input_string = input_string + secret_string
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()
    return hashed_string


def __check_authorized_user(email_encrypted, AUTHORIZED_USERS):
    email = __symmetric_decrypt(email_encrypted)
    if email in AUTHORIZED_USERS or '*@' + email.split('@')[1] in AUTHORIZED_USERS:
        __set_cookie('streamlit_auth_cookie', True, key='set_streamlit_auth_cookie')
        __set_cookie('email_encrypted', email_encrypted, key='set_email')
        __set_cookie('email_secret', __hasher(email), key='set_email_secret')
    else:
        st.write('Unauthorized user, please request access.')


def __symmetric_encrypt(input_string, secret_string=os.getenv('FERNET_KEY')):
    cipher_suite = Fernet(secret_string)
    encrypted_value = cipher_suite.encrypt(input_string.encode()).decode()
    return encrypted_value

def __symmetric_decrypt(input_string, secret_string=os.getenv('FERNET_KEY')):
    cipher_suite = Fernet(secret_string)
    decrypted_value = cipher_suite.decrypt(input_string.encode()).decode()
    return decrypted_value


#%% Google OAuth Functions

def __login(flow):
    authorization_url, state = flow.authorization_url()
    html_content = f"""
<div style="display: flex; justify-content: "center";">
<a href="{authorization_url}" target="_self" style="background-color: '#4285f4'; color: '#fff'; text-decoration: none; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; padding: 8px 12px; border-radius: 4px; display: flex; align-items: center;">
<img src="https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA" alt="Google logo" style="margin-right: 8px; width: 26px; height: 26px; background-color: white; border: 2px solid white; border-radius: 4px;">
Sign in with Google
</a>
</div>
"""
    st.title("Mastermind Reporting")
    st.markdown(html_content, unsafe_allow_html=True)
    

def __callback(flow):
    auth_code = st.query_params.get("code")
    st.query_params.clear()
    flow.fetch_token(code=auth_code)
    credentials = flow.credentials

    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    email_encrypted = __symmetric_encrypt(user_info.get('email'))
    __set_session_var('email_encrypted', email_encrypted)


#%% Create Wrapper

def authenticate(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):

        AUTHORIZED_USERS = os.getenv('AUTHORIZED_USERS')
        CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILE')
        REDIRECT_URI = os.getenv('REDIRECT_URI')

        AUTHORIZED_USERS = AUTHORIZED_USERS.split(',')
        AUTHORIZED_USERS = [x.strip() for x in AUTHORIZED_USERS]

        if 'is_authorized' not in st.session_state:
            __set_session_var('is_authorized', False)

        if 'cookie_manager' not in st.session_state:
            __set_session_var('cookie_manager', CookieManager(key="combined"))

        if 'id_token' not in st.session_state:
            __set_session_var('id_token', None)

        if 'email_encrypted' not in st.session_state:
            __set_session_var('email_encrypted', None)

        if st.session_state['is_authorized'] == False:
            __set_session_var('is_authorized', __ensure_cookie("streamlit_auth_cookie", True))

        if st.session_state['is_authorized'] == True:
            if st.session_state['email_encrypted'] == None:
                __set_session_var('email_encrypted', st.session_state['cookie_manager'].get('email_encrypted'))

            email_encrypted = st.session_state.get('email_encrypted')
            email = __symmetric_decrypt(email_encrypted)
            if __hasher(email) == st.session_state['cookie_manager'].get('email_secret'):
                func(*args, **kwargs)
            else:
                st.write("Your cookies have been tampered with, please clear your cookies and try again.")

        else:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                client_secrets_file = CLIENT_SECRETS_FILE,
                scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
                redirect_uri=REDIRECT_URI,
            )
            if st.session_state['email_encrypted'] == None and st.query_params.get("code") != None:
                __callback(flow)
            elif st.session_state['email_encrypted'] == None:
                __login(flow)

            if st.session_state['email_encrypted'] != None:
                __check_authorized_user(st.session_state.get('email_encrypted'), AUTHORIZED_USERS)

    return wrapper_decorator


#%%

if __name__ == "__main__":
    @authenticate
    def main():
        st.title('Working Smoothly!')

    main()


#%%