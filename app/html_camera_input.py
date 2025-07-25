try:
    import streamlit as st
except ModuleNotFoundError as exc:
    raise ImportError(
        "streamlit is required for the CAP app. "
        "Install dependencies using `pip install -r requirements.txt`."
    ) from exc


def back_camera_uploader(label="Take a picture"):
    """Use a file uploader that requests the back camera on mobile."""
    uploader = st.file_uploader(label, type=["png", "jpg", "jpeg"], key="camera")
    st.markdown(
        """
        <script>
        const inputs = window.parent.document.querySelectorAll('input[type="file"]');
        inputs.forEach(el => el.setAttribute('capture', 'environment'));
        </script>
        """,
        unsafe_allow_html=True,
    )
    return uploader
