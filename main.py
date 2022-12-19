"""streamlit app entry point"""
import streamlit as st
from components import footer
from sub_pages import acag, caces, radon, hisdac_county, hisdac_fbuy

DATASETS = {
    "ACAG": acag,
    "CACES": caces,
    "Radon": radon,
    "HISDAC-County": hisdac_county,
    "HISDAC-FBUY": hisdac_fbuy
}

st.title("CEDaR")

# Sidebar
st.sidebar.title('DATASETS')
selection = st.sidebar.radio('DATASETS', list(DATASETS.keys()), label_visibility="collapsed")
page = DATASETS[selection]
page.app()

footer.add_footer()
