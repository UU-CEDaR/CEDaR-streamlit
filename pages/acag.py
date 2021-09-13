import streamlit as st
from streamlit_folium import folium_static
import folium
import xarray as xr
import numpy as np
from datetime import datetime, date, timedelta


@st.cache
def data_array(comp, year, data_path):
    ds = xr.open_zarr(data_path+"/duace/annual.zarr")
    # ds = xr.open_dataset("gcs://cedar-datasets/duace/annual.zarr",
    #     backend_kwargs={
    #         "storage_options": {"project": "cedar-283904", "token": None}
    #     },
    #     engine="zarr",
    # )
    return ds[comp].loc[f"{year}-01-01"].data

def app(data_path):
    st.write("## ACAG")
    st.write("Ground-level composition mass concentrations estimation from [ACAG](https://sites.wustl.edu/acag/).")
    comp = st.selectbox("Composition:", ['BC', 'NH4', 'NIT', 'OM', 'PM25', 'SO4', 'SOIL', 'SS'])
    sel_year = st.slider(
        "Year:",
        min_value=2000,
        max_value=2017,
        value=2010)

    data = data_array(comp, sel_year, data_path)

    m = folium.Map(location=[39.949610, -111.0],
                    min_zoom=6,
                    max_zoom=10,
                    zoom_start=6,
                    fadeAnimation=False)

    m.add_child(folium.raster_layers.ImageOverlay(data, 
                opacity=.7, 
                bounds = [[36.99, -114.05], [42.01, -109.04]]))

    # call to render Folium map in Streamlit
    folium_static(m)