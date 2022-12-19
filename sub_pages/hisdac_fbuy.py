"""Drwa page for Historical settlement dataset."""
import branca.colormap as colormap
import folium
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import xarray as xr
from streamlit_folium import folium_static
# pylint: disable=invalid-name, line-too-long

cm = plt.cm.get_cmap('viridis_r')
TIFFFILES = {
    "First built-up year": "FBUY_LZW.tif",
    "Inside positional uncertainty": "FBUY_IPU_PACKBITS.tif",
    "Outside positional uncertainty": "FBUY_OPU_PACKBITS.tif",
    "Overall positional uncertainty": "FBUY_OPPU_PACKBITS.tif"
}
CAPTION = {
    "First built-up year": "First built-up (year)",
    "Inside positional uncertainty": "Inside positional uncertainty",
    "Outside positional uncertainty": "Outside positional uncertainty",
    "Overall positional uncertainty": "Overall positional uncertainty"
}

@st.cache
def load_data(attr):
    """Load dataset."""
    # ds = xr.open_zarr("data/hap_annual.zarr")
    ds = xr.open_rasterio(f"data/hisdac/{TIFFFILES[attr]}")
    data = ds.data[0]
    x, y = data.shape
    bounds = [[ds.transform[5]+ds.transform[4]*y, ds.transform[2]], [ds.transform[5], ds.transform[2]+ds.transform[0]*x]]
    if attr == "First built-up year":
        data = data.astype(np.single)
        data = np.ma.masked_array(data, mask=np.logical_or(data==0, data==1))
    else:
        data = np.ma.masked_array(data, data==0)
    data = (data - data.min()) / (data.max() - data.min()) # normalize
    return cm(data), data.min(), data.max(), bounds

def app():
    """Draw the page."""
    st.write("## HISDAC - FBUY")
    st.write("Reprejected Utah area of Historical settlement composite layer for the U.S. 1810 - 2015. Contained in the dataverse [HISDAC-US](https://dataverse.harvard.edu/dataverse/hisdacus).")
    attr = st.selectbox("Attribute:", list(TIFFFILES.keys()))
    image, vmin, vmax, bounds = load_data(attr)

    fmap = folium.Map(location=[39.6, -111.5],
                   min_zoom=6, max_zoom=12, zoom_start=7)

    fmap.add_child(folium.raster_layers.ImageOverlay(image,
                opacity=.7, mercator_project=True,
                bounds = bounds))

    color_list = [cm(i) for i in np.linspace(0,1,num=10)]
    legend = colormap.LinearColormap(color_list, caption=CAPTION[attr]).scale(vmin=vmin, vmax=vmax)
    fmap.add_child(legend)
    folium_static(fmap, width=700, height=800)
