import streamlit as st
from streamlit_folium import folium_static
import folium
import xarray as xr
import numpy as np
from datetime import datetime, date, timedelta
import footer
import categories

# Header area
st.markdown('<a href="/" target = "_self"> <h1> CEDaR </h1> </a>', unsafe_allow_html=True)
st.markdown('A description of CEDaR.')

# Main area
params = st.experimental_get_query_params()
categories.run(params)

# Footer area
footer.footer("This project is supported by a UofU HCI CCPS pilot grant and by NSF Award IIS-1816149.")
