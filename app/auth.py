import streamlit as st
from auth0_component import login_button

AUTH0_CLIENT_ID = None
AUTH0_DOMAIN = None

if "auth0" in st.secrets:
    AUTH0_CLIENT_ID = st.secrets["auth0"].get("client_id")
    AUTH0_DOMAIN = st.secrets["auth0"].get("domain")


def authenticate():
    if not AUTH0_CLIENT_ID or not AUTH0_DOMAIN:
        st.error("Auth0 configuration missing")
        st.stop()

    token = login_button(client_id=AUTH0_CLIENT_ID, domain=AUTH0_DOMAIN)
    if token:
        st.session_state["token"] = token
        return True
    return False
