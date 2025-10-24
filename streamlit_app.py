from pathlib import Path
from typing import Optional, Union
import streamlit as st

# Resolve paths relative to this file (works on Streamlit Cloud & locally)
APP_DIR = Path(__file__).resolve().parent
PROFILE_IMG_PATH = APP_DIR / "static" / "habib.jpeg"
FALLBACK_AVATAR_URL = "https://via.placeholder.com/300x300.png?text=Profile"

@st.cache_data(ttl=60 * 60)  # cache for 1 hour
def _read_image_bytes(p: Path) -> Optional[bytes]:
    """Read image bytes safely; return None on any failure."""
    try:
        return p.read_bytes()
    except Exception:
        return None

def get_profile_image_src() -> Union[bytes, str]:
    """
    Return bytes for the local image if it exists *and* is readable.
    Otherwise return a fallback URL. This keeps the app from crashing.
    """
    data = _read_image_bytes(PROFILE_IMG_PATH)
    return data if data else FALLBACK_AVATAR_URL
