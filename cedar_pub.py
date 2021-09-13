import streamlit as st
from streamlit_folium import folium_static
import folium
import xarray as xr
import numpy as np
from datetime import datetime, date, timedelta
from pages import acag, caces, radon, hisdac_county, hisdac_fbuy

data_path = "data"

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
page.app(data_path)