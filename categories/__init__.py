import streamlit as st
import importlib
import pkgutil

def run(params):
    if "category" in params.keys() and params["category"][0] != "Home":
        #Run the module that you want...
        importlib.import_module(__name__+"."+params["category"][0]).run(params)
    else:
        st.write("## Categories")
        #Write down the categories as default.
        for importer, name, _ in pkgutil.iter_modules(__path__, __name__+"."):
            module = importlib.import_module(name)
            # st.write(f"* [{category_module.name}]({category_module.link})")
            st.markdown(f'<a href="{module.link}" target = "_self"> {module.name} </a>', unsafe_allow_html=True)
