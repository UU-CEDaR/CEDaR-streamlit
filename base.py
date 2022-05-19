import streamlit as st
from streamlit_folium import folium_static
import folium
import xarray as xr
import numpy as np
from datetime import datetime, date, timedelta
from categories.category_a import caces
import footer
from pages import acag, radon, hisdac_county, hisdac_fbuy

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
selection = st.sidebar.radio('', list(DATASETS.keys()))
page = DATASETS[selection]
page.app()

footer.footer("This project is supported by a UofU HCI CCPS pilot grant and by NSF Award IIS-1816149.")
