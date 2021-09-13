import streamlit as st
from streamlit_folium import folium_static
import folium
import xarray as xr
import numpy as np
from datetime import datetime, date, timedelta
import geopandas
import pandas as pd

SHAPEFILES = {
    "counties": "tl_2010_49_county10.shz",
    "tracts": "tl_2010_49_tract10.shz",
    "blockgroups": "tl_2010_49_bg10.shz"
}

@st.cache
def load_data(data_path):
    gdf = geopandas.read_file(data_path+'/hisdac/County_level_uncertainty_Utah.shz')
    return gdf
    # ['GEOID', 'NAME', 'NumRecords', 'TMiss', 'GeoMiss', 'LUMiss', 'AMiss',
    #    'geometry']

def app(data_path):
    st.write("## HISDAC - County")
    st.write("County-level uncertainty statistics accompanying the historical settlement.")
    comp = st.selectbox("Attribute:", ['NumRecords', 'TMiss', 'GeoMiss', 'LUMiss', 'AMiss'])
    gdf = load_data(data_path)

    m = folium.Map(location=[39.949610, -111.0],
                    min_zoom=6,
                    max_zoom=12,
                    zoom_start=6)

    folium.Choropleth(
        geo_data=gdf,
        data=gdf,
        columns=["GEOID", comp],
        key_on='feature.properties.GEOID',
        fill_color="OrRd",
        nan_fill_color='red',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="",
    ).add_to(m)
    
    folium_static(m)