import streamlit as st
import importlib
import pkgutil
import os
import categories.category_a
from classes.category_class import category_class

name = "Category A"
link = "./?category=category_a"

def run(params, page_configurations):
    cat = category_class(name="Category A", 
        description = "A sample category for testing visualizations.",
        path = os.path.dirname(categories.category_a.__file__),
    )
    
    cat.page()

    params = st.experimental_get_query_params()

    if "dataset" in params.keys() and params["dataset"][0] != "Description":
            importlib.import_module(__name__ + '.'  +params["dataset"][0]).run(params, page_configurations)
            return
    for _, name, _ in pkgutil.iter_modules(__path__, __name__+'.'):
        module = importlib.import_module(name)
        st.markdown(f'<a href="{module.link}" target = "_self"> {module.name} </a>', unsafe_allow_html=True)
