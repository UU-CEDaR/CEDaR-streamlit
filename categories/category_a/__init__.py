import streamlit as st
import importlib
import pkgutil
import sys

name = "Category A"
link = "./?category=category_a"

def run(params):
    st.write("## Category A")
    st.write("A description of category A.")
    if "dataset" in params.keys():
        importlib.import_module(__name__ + '.' +params["dataset"][0]).run(params)
        return
    for _, name, _ in pkgutil.iter_modules(__path__, __name__+'.'):
        module = importlib.import_module(name)
        st.markdown(f'<a href="{module.link}" target = "_self"> {module.name} </a>', unsafe_allow_html=True)
