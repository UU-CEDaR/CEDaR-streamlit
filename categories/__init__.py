import streamlit as st
import importlib
import pkgutil

def run(params, page_configurations):
    if "category" in params.keys() and params["category"][0] != "Home":
        #Run the module that you want...
        importlib.import_module(__name__+"."+params["category"][0]).run(params, page_configurations)
    else:
        st.write("## <- Click on one of the tabs to get started")
