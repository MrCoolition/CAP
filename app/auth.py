import os
import streamlit as st
from auth0_component import login_button

AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")


def authenticate():
    if not AUTH0_CLIENT_ID or not AUTH0_DOMAIN:
        st.error("Auth0 configuration missing")
        st.stop()

    token = login_button(client_id=AUTH0_CLIENT_ID, domain=AUTH0_DOMAIN)
    if token:
        st.session_state["token"] = token
        return True
    return False
