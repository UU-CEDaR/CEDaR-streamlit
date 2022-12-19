"""Show radon dataset."""
import folium
import geopandas
import streamlit as st
from streamlit_folium import folium_static

SHAPEFILES = {
    "counties": "tl_2010_49_county10.shp.zip",
    "tracts": "tl_2010_49_tract10.shp.zip",
    "blockgroups": "tl_2010_49_bg10.shp.zip"
}

@st.cache(allow_output_mutation=True)
def load_data():
    """Load dataset."""
    gdf = geopandas.read_file('data/Radon_High_ZIP_code.shp.zip', driver='ESRI Shapefile')
    return gdf
    # ['FID_ZipCod', 'ZIP5', 'COUNTYNBR', 'NAME', 'SYMBOL', 'SHAPE_Leng',
    #    'SHAPE_Area', 'Shape_Ar_1', 'FID_Radon_', 'OBJECTID_1', 'COUNTYNB_1',
    #    'ENTITYNBR', 'ENTITYYR', 'NAME_1', 'FIPS', 'STATEPLANE', 'POP_LASTCE',
    #    'POP_CURRES', 'GlobalID', 'FIPS_STR', 'COLOR4', 'Shape_ar_2',
    #    'Shape_len', 'RADPOT', 'HighEP_Are', 'OBJECTID', 'FID_ZipC_1', 'ZIP5_1',
    #    'COUNTYNB_2', 'NAME_12', 'FREQUENCY', 'SUM_HighEP', 'FIRST_Shap',
    #    'Perc_HighR', 'geometry']

def app():
    """Show page for radon dataset."""
    st.write("## Radon")
    st.write("Radon High Zip code.")
    comp = st.selectbox("Attribute:", ['FREQUENCY', 'SUM_HighEP', 'Perc_HighR'])
    gdf = load_data()

    fmap = folium.Map(location=[39.6, -111.5],
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
    ).add_to(fmap)

    folium_static(fmap, width=700, height=800)
