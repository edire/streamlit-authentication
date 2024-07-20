
import os
import streamlit as st
from extra_streamlit_components import CookieManager
from time import sleep

if 'session_num' not in st.session_state:
    st.session_state['session_num'] = 0
else:
    st.session_state['session_num'] += 1

session_num = st.session_state['session_num']
sleep(2)

if session_num == st.session_state['session_num']:

    cookie_timing = float(os.getenv('COOKIE_TIMING', 0.25))


    def __set_session_var(name, var):
        sleep(cookie_timing)
        st.session_state[name] = var


    if 'cookie_manager' not in st.session_state:
        __set_session_var('cookie_manager', CookieManager(key="combined"))


    print(session_num)

    st.title('ARK')