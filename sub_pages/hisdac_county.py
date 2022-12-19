"""Show historical settlement uncertainty dataset."""
import folium
import geopandas
import streamlit as st
from streamlit_folium import folium_static

@st.cache(allow_output_mutation=True)
def load_data():
    """Load dataset."""
    filename = 'data/hisdac/County_level_uncertainty_Utah.shp.zip'
    gdf = geopandas.read_file(filename, driver='ESRI Shapefile')
    return gdf
    # ['GEOID', 'NAME', 'NumRecords', 'TMiss', 'GeoMiss', 'LUMiss', 'AMiss',
    #    'geometry']

def app():
    """Draw the page."""
    st.write("## HISDAC - County")
    st.write("County-level uncertainty statistics accompanying the historical settlement.")
    comp = st.selectbox("Attribute:", ['NumRecords', 'TMiss', 'GeoMiss', 'LUMiss', 'AMiss'])
    gdf = load_data()

    fmap = folium.Map(location=[39.6, -111.5],
                   min_zoom=6, max_zoom=12, zoom_start=7)

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
    ).add_to(fmap)

    folium_static(fmap, width=700, height=800)
