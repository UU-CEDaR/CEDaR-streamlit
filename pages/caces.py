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
def load_shapes(shape, data_path):
    gdf = geopandas.read_file(data_path+f'/census/{SHAPEFILES[shape]}')
    gdf = gdf[['GEOID10','NAMELSAD10','geometry']]#.rename(columns={'GEOID10':'feature.id'})
    return gdf

@st.cache
def load_data(shape, comp, year, data_path):
    df = pd.read_csv(data_path + f"/caces/utah-{shape}.csv")
    df = df[(df.year==year) & (df.pollutant==comp)][['fips','pred_wght']].astype({'fips':'str'})
    return df

def app(data_path):
    st.write("## CACES - LUR")
    st.write("Land Use Regression models from [CACES](https://www.caces.us/).")
    shape = st.selectbox("Resolution:", list(SHAPEFILES.keys()))
    comp = st.selectbox("Pollutant:", ['co', 'no2', 'o3', 'pm10', 'pm25', 'so2'])
    year = st.slider(
        "Year:",
        min_value=1979,
        max_value=2015,
        value=2010)
    df = load_data(shape, comp, year, data_path)
    gdf = load_shapes(shape, data_path)

    m = folium.Map(location=[39.949610, -111.0],
                    min_zoom=6,
                    max_zoom=12,
                    zoom_start=6)
    # folium.GeoJson(data=gdf["geometry"]).add_to(m)
    folium.Choropleth(
        geo_data=gdf,
        data=df,
        columns=["fips", "pred_wght"],
        key_on='feature.properties.GEOID10',
        fill_color="OrRd",
        nan_fill_color='red',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="",
    ).add_to(m)
    # call to render Folium map in Streamlit
    folium_static(m)