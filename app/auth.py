import logging
import streamlit as st
from auth0_component import login_button

logger = logging.getLogger(__name__)

AUTH0_CLIENT_ID = None
AUTH0_DOMAIN = None

if "auth0" in st.secrets:
    AUTH0_CLIENT_ID = st.secrets["auth0"].get("client_id")
    AUTH0_DOMAIN = st.secrets["auth0"].get("domain")


def authenticate():
    if not AUTH0_CLIENT_ID or not AUTH0_DOMAIN:
        logger.error("Auth0 configuration missing")
        st.error("Auth0 configuration missing")
        st.stop()

    # pass credentials positionally to avoid mismatched keyword names
    logger.info("Attempting Auth0 login via %s", AUTH0_DOMAIN)
    token = login_button(AUTH0_CLIENT_ID, AUTH0_DOMAIN)
    if token:
        st.session_state["token"] = token
        logger.info("Auth0 login succeeded")
        return True

    logger.error("Auth0 login failed: no token returned")
    st.error("Login failed. Check Auth0 callback URLs.")
    return False
