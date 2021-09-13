import streamlit as st
from streamlit_folium import folium_static
import folium
import xarray as xr
import numpy as np
from datetime import datetime, date, timedelta

TIFFFILES = {
    "First built-up year": "FBUY_LZW.tif",
    "Inside positional uncertainty": "FBUY_IPU_PACKBITS.tif",
    "Outside positional uncertainty": "FBUY_OPU_PACKBITS.tif",
    "Overall positional uncertainty": "FBUY_OPPU_PACKBITS.tif"
}

@st.cache
def load_data(attr, data_path):
# ds = xr.open_zarr("data/hap_annual.zarr")
    ds = xr.open_rasterio(data_path+f"/hisdac/{TIFFFILES[attr]}")
    return ds.data[0]

def app(data_path):
    st.write("## HISDAC - FBUY")
    st.write("Reprejected Utah area of Historical settlement composite layer for the U.S. 1810 - 2015. Contained in the dataverse [HISDAC-US](https://dataverse.harvard.edu/dataverse/hisdacus).")
    attr = st.selectbox("Attribute:", list(TIFFFILES.keys()))
    data = load_data(attr, data_path)

    m = folium.Map(location=[39.949610, -111.0],
                    min_zoom=6, max_zoom=10, zoom_start=6,
                    crs='EPSG3857')

    m.add_child(folium.raster_layers.ImageOverlay(data,
                opacity=.7, 
                bounds = [[36.99, -114.05], [42.01, -109.04]]))

    folium_static(m)