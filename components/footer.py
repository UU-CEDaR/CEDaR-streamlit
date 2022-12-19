"""Add footer to page."""
import streamlit as st
FOOTER_STYLE="""<style>
.footer {
    opacity: 0.5;
    font-size: 0.8rem;
    position: fixed;
    right: 0;
    bottom: 0;
    padding: 0.5rem 1rem;
    text-align: right;
}
</style>
"""
CREDITS = "This project is supported by a UofU HCI CCPS pilot grant and by NSF Award IIS-1816149."

def add_footer():
    """Add credits to current page."""
    html = f"<div class='footer'>{CREDITS}</div>"
    st.markdown(FOOTER_STYLE+html, unsafe_allow_html=True)
