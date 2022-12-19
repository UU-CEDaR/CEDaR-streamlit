"""Show caces dataset."""
import copy

import folium
import geopandas
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

# pylint: disable=invalid-name

SHAPEFILES = {
    "counties": "tl_2010_49_county10.shp.zip",
    "tracts": "tl_2010_49_tract10.shp.zip",
    "blockgroups": "tl_2010_49_bg10.shp.zip"
}
CAPTION = {
    'co': 'CO (ppb)',
    'no2': 'NO₂ (ppb)',
    'o3': 'O₃ (ppb)',
    'pm10': 'PM₁₀ (μg/m³)',
    'pm25': 'PM₂₅ (μg/m³)',
    'so2': 'SO₂ (ppm)'
}
RANGE = {
    'co': [1990,2015],
    'no2': [1979,2015],
    'o3': [1979,2015],
    'pm10': [1988,2015],
    'pm25': [1999,2015],
    'so2': [1979,2015]
}

@st.cache
def load_shapes(shape):
    """Load shapes of counties, tracts, or blockgroups."""
    gdf = geopandas.read_file(f'data/census/{SHAPEFILES[shape]}', driver='ESRI Shapefile')
    gdf = gdf[['GEOID10','NAMELSAD10','geometry']]#.rename(columns={'GEOID10':'feature.id'})
    return gdf

@st.cache
def load_data(shape, comp, year):
    """Load dataset for a given shape, component, and year."""
    df = pd.read_csv(f"data/caces/utah-{shape}.csv")
    df = df[(df.year==year) & (df.pollutant==comp)][['fips','pred_wght']].astype({'fips':'str'})
    return df

def app():
    """Show page for caces dataset."""
    st.write("## CACES - LUR")
    st.write("Land Use Regression models from [CACES](https://www.caces.us/).")
    shape = st.selectbox("Resolution:", list(SHAPEFILES.keys()))
    comp = st.selectbox("Pollutant:", ['co', 'no2', 'o3', 'pm10', 'pm25', 'so2'])
    year = st.slider(
        "Year:",
        min_value=RANGE[comp][0],
        max_value=RANGE[comp][1],
        value=RANGE[comp][1])
    df = load_data(shape, comp, year)
    gdf = copy.deepcopy(load_shapes(shape))
    # gdf = load_shapes(shape).copy()

    m = folium.Map(location=[39.6, -111.5],
                   min_zoom=6, max_zoom=12, zoom_start=7)
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
        legend_name=CAPTION[comp],
    ).add_to(m)
    # call to render Folium map in Streamlit
    folium_static(m, width=700, height=800)
