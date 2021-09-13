import streamlit as st
from streamlit_folium import folium_static
import folium
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date, timedelta
import branca.colormap as colormap

cm = plt.cm.get_cmap('viridis_r')

@st.cache
def load_data(comp, year, data_path):
    ds = xr.open_zarr(data_path+"/duace/annual.zarr")
    # ds = xr.open_dataset("gcs://cedar-datasets/duace/annual.zarr",
    #     backend_kwargs={
    #         "storage_options": {"project": "cedar-283904", "token": None}
    #     },
    #     engine="zarr",
    # )
    caption = f'{ds[comp].standard_name} ({ds[comp].units})'
    data = ds[comp].loc[f"{year}-01-01"].data
    min, max = data.min(), data.max()
    data = (data - data.min()) / (data.max() - data.min()) # normalize
    return cm(data), min, max, caption

def app(data_path):
    st.write("## ACAG")
    st.write("Ground-level composition mass concentrations estimation from [ACAG](https://sites.wustl.edu/acag/).")
    comp = st.selectbox("Composition:", ['BC', 'NH4', 'NIT', 'OM', 'PM25', 'SO4', 'SOIL', 'SS'])
    sel_year = st.slider(
        "Year:",
        min_value=2000,
        max_value=2017,
        value=2010)

    image, min, max, caption = load_data(comp, sel_year, data_path)

    m = folium.Map(location=[39.949610, -111.0],
                    min_zoom=6, max_zoom=10, zoom_start=6)

    m.add_child(folium.raster_layers.ImageOverlay(image, 
                opacity=.7, mercator_project=True,
                bounds = [[36.99, -114.05], [42.01, -109.04]]))

    color_list = [cm(i) for i in np.linspace(0,1,num=10)]
    legend = colormap.LinearColormap(color_list, caption=caption).scale(vmin=min, vmax=max)
    m.add_child(legend)
    # call to render Folium map in Streamlit
    folium_static(m)