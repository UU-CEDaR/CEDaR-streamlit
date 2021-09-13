import streamlit as st
style="""<style>
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
def footer(text):
    contant = f"<div class='footer'>{text}</div>"
    st.markdown(style+contant, unsafe_allow_html=True)