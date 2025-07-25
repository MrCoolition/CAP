try:
    import streamlit as st
except ModuleNotFoundError as exc:
    raise ImportError(
        "streamlit is required for the CAP app. "
        "Install dependencies using `pip install -r requirements.txt`."
    ) from exc


def back_camera_input(label="Take a picture", **kwargs):
    """Capture an image using the device's back camera when possible."""
    try:
        return st.camera_input(label, facing_mode="environment", **kwargs)
    except TypeError:
        # ``facing_mode`` not supported in older Streamlit versions
        return st.camera_input(label, **kwargs)
