import streamlit as st


def back_camera_input(label="Take a picture", **kwargs):
    """Capture an image using the device's back camera when possible."""
    try:
        return st.camera_input(label, facing_mode="environment", **kwargs)
    except TypeError:
        # ``facing_mode`` not supported in older Streamlit versions
        return st.camera_input(label, **kwargs)
