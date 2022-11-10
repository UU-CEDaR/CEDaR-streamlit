from unicodedata import category
import streamlit as st
import importlib
import pkgutil
import sys
import os
import categories.Chemical_Waste
from classes.category_class import category_class

name = "ChemicalWaste"
link = "./?category=ChemicalWaste"


def run(params, page_configurations):

    cat = category_class(name="Chemical Hazardous Waste", 
        description = "This dataset has a bunch of datasets describing\nthe nature of chemical hazardous waste around\nthe US and Utah.",
        path = os.path.dirname(categories.Chemical_Waste.__file__),
    )
    
    cat.page()

    params = st.experimental_get_query_params()

    if "dataset" in params.keys() and params["dataset"][0] != "Description":
            importlib.import_module(__name__ + '.'  +params["dataset"][0]).run(params, page_configurations)
            return
    for _, name, _ in pkgutil.iter_modules(__path__, __name__+'.'):
        module = importlib.import_module(name)
        st.markdown(f'<a href="{module.link}" target = "_self"> {module.name} </a>', unsafe_allow_html=True)

