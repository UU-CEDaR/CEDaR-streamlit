import streamlit as st
from streamlit_folium import folium_static
import folium
import xarray as xr
import numpy as np
from datetime import datetime, date, timedelta
import footer
import categories
import pkgutil
import os

def getCategories():
    theList = ['Home']
    pkgpath = os.path.dirname(categories.__file__)
    for _, name, _ in pkgutil.iter_modules([pkgpath]):
        theList.append(name)
    return theList


# Header area
st.markdown('<a href="/" target = "_self"> <h1> CEDaR </h1> </a>', unsafe_allow_html=True)
st.markdown('A description of CEDaR.')

#CATEGORIES is going to be the list of names of categories under the categories folder.
#Clicking on one of the categories in the radio list will take you to that particular category page.
CATEGORIES = getCategories()

st.sidebar.title('CATEGORIES')
selection = st.sidebar.radio('', CATEGORIES)

if (selection != "Home"):
    st.experimental_set_query_params(
        category=selection
    )
else:
    st.experimental_set_query_params(

    )

# Main area
params = st.experimental_get_query_params() #returns the params in the url as a dictionary... eg "category: chw"
categories.run(params)



# Footer area
footer.footer("This project is supported by a UofU HCI CCPS pilot grant and by NSF Award IIS-1816149.")
