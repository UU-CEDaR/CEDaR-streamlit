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
import yaml
import urllib
from classes.high_level_csv_page import DatasetPageCreator


def defaultDisplayHome():
    st.write("## <- Click on one of the tabs to get started")

def getCategory(categorySelection, CATEGORIES):
    for i in CATEGORIES:
        if (categorySelection == i['name']):
            return i
    return None

def getDataset(datasetSelection, DATASETS):
	for i in DATASETS:
		if (datasetSelection == i['datasetName']):
			return i
	return None
	
def categoryDisplayHome():
    st.write("## <- Choose a dataset from the menu")
    
    


# Header area
st.markdown('<a href="/" target = "_self"> <h1> CEDaR </h1> </a>', unsafe_allow_html=True)
st.markdown('A description of CEDaR.')

#CATEGORIES is going to be the list of names of categories under the categories folder.
#Clicking on one of the categories in the radio list will take you to that particular category page.
#CATEGORIES = getCategories()

f = urllib.request.urlopen('https://storage.googleapis.com/cedar-datasets/cedar_config.yml')

page_configurations = yaml.safe_load(f.read())

CATEGORIES = page_configurations['categories'] #List of dictionaries
radioCategories = ['Home']
for i in CATEGORIES:
    radioCategories.append(i['name'])
categorySelection = st.sidebar.radio('', radioCategories)

if (categorySelection == "Home") or categorySelection not in radioCategories:
	defaultDisplayHome()

else:
	#perhaps put this into a 'displayOneCategory' function...
	category = getCategory(categorySelection, CATEGORIES) #The category with the name that matches the current configuration
	DATASETS = category['datasets']
	radioDatasets = ['Home']
	for i in DATASETS:
		radioDatasets.append(i['datasetName'])
	datasetSelection = st.sidebar.radio('', radioDatasets)
	if (datasetSelection == "Home") or datasetSelection not in radioDatasets:
		categoryDisplayHome()
	else:
		page = DatasetPageCreator(getDataset(datasetSelection, DATASETS))
		page.loadPage()
footer.footer("This project is supported by a UofU HCI CCPS pilot grant and by NSF Award IIS-1816149.")
#
#st.sidebar.title('CATEGORIES')
#selection = st.sidebar.radio('', CATEGORIES)
#
#if (selection != "Home"):
#    st.experimental_set_query_params(
#        category=selection
#    )
#else:
#    st.experimental_set_query_params(
#
#    )
#
# Main area
#params = st.experimental_get_query_params() #returns the params in the url as a dictionary... eg "category: chw"
#categories.run(params, page_configurations)

#If "category" in params.keys() and params["category"][0] != "Home": Keep going. Otherwise stop and display a message.
#

