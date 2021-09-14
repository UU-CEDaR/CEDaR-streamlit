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
    gdf = geopandas.read_file(data_path+'/Radon_High_ZIP_code.shz')
    return gdf
    # ['FID_ZipCod', 'ZIP5', 'COUNTYNBR', 'NAME', 'SYMBOL', 'SHAPE_Leng',
    #    'SHAPE_Area', 'Shape_Ar_1', 'FID_Radon_', 'OBJECTID_1', 'COUNTYNB_1',
    #    'ENTITYNBR', 'ENTITYYR', 'NAME_1', 'FIPS', 'STATEPLANE', 'POP_LASTCE',
    #    'POP_CURRES', 'GlobalID', 'FIPS_STR', 'COLOR4', 'Shape_ar_2',
    #    'Shape_len', 'RADPOT', 'HighEP_Are', 'OBJECTID', 'FID_ZipC_1', 'ZIP5_1',
    #    'COUNTYNB_2', 'NAME_12', 'FREQUENCY', 'SUM_HighEP', 'FIRST_Shap',
    #    'Perc_HighR', 'geometry']

def app(data_path):
    st.write("## Radon")
    st.write("Radon High Zip code.")
    comp = st.selectbox("Attribute:", ['FREQUENCY', 'SUM_HighEP', 'Perc_HighR'])
    gdf = load_data(data_path)

    m = folium.Map(location=[39.6, -111.5],
                   min_zoom=6, max_zoom=12, zoom_start=7)

    folium.Choropleth(
        geo_data=gdf,
        data=gdf,
        columns=["FID_ZipCod", comp],
        key_on='feature.properties.FID_ZipCod',
        fill_color="OrRd",
        nan_fill_color='red',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="",
    ).add_to(m)

    folium_static(m, width=700, height=800)