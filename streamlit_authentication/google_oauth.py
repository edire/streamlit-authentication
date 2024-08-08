#%% Import Libraries

import os
import streamlit as st
import functools
import _google_oauth as ga
import _tools
from extra_streamlit_components import CookieManager
import datetime as dt


#%% Create Wrapper

def authenticate(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):

        cookie_manager = CookieManager(key="combined")
        def set_cookie(cookie_name, cookie_value, secure=True, same_site="None", expires_at = dt.datetime.now() + dt.timedelta(days=30)):
            cookie_manager.set(cookie_name, cookie_value, key=f'set_{cookie_name}', secure=secure, same_site=same_site, expires_at = expires_at)
        email_encrypted = cookie_manager.get('email_encrypted')
        email_secret = cookie_manager.get('email_secret')

        if 'rerun' not in st.session_state:
            st.session_state['rerun'] = 0
        if email_encrypted and email_secret:
            email = _tools.symmetric_decrypt(email_encrypted)
            email_hash = _tools.hash_encrypt(email)
            if email_hash == email_secret:
                func(*args, **kwargs)
            else:
                st.write("Your cookies have been tampered with, please clear your cookies and try again.")
        else:
            if st.query_params.get("code") != None:
                email = ga.callback()
                AUTHORIZED_USERS = os.getenv('AUTHORIZED_USERS', '*')
                is_authorized = _tools.check_authorized_user(email, AUTHORIZED_USERS)
                if is_authorized:
                    email_encrypted = _tools.symmetric_encrypt(input_string=email)
                    set_cookie(cookie_name='email_encrypted', cookie_value=email_encrypted)
                    set_cookie(cookie_name='email_secret', cookie_value=is_authorized)
                else:
                    st.write('Unauthorized user, please request access.')
            else:
                if st.session_state['rerun'] <= 2:
                    st.session_state['rerun'] += 1
                    st.rerun()
                ga.login()

    return wrapper_decorator


#%%

if __name__ == "__main__":
    @authenticate
    def main():
        st.title('Working Smoothly!')

    main()


#%%