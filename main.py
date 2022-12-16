"""App entry point."""

import urllib

import streamlit as st
import yaml

import footer
from classes.high_level_csv_page import DatasetPageCreator


# pylint: disable=missing-function-docstring, invalid-name, line-too-long
def defaultDisplayHome():
    st.write("## <- Click on one of the tabs to get started")

def getCategory(category_name, cagegories):
    for c in cagegories:
        if category_name == c['name']:
            return c
    return None

def getDataset(dataset_name, datasets):
    for d in datasets:
        if dataset_name == d['datasetName']:
            return d
    return None

def categoryDisplayHome():
    st.write("## <- Choose a dataset from the menu")


config_filename = 'https://storage.googleapis.com/cedar-datasets/cedar_config.yml'

# Header area
st.markdown('<a href="/" target = "_self"> <h1> CEDaR </h1> </a>', unsafe_allow_html=True)
st.markdown('A description of CEDaR.')

#CATEGORIES is going to be the list of names of categories under the categories folder.
#Clicking on one of the categories in the radio list will take you to that particular category page.
#CATEGORIES = getCategories()

f = urllib.request.urlopen(config_filename)

page_configurations = yaml.safe_load(f.read())

CATEGORIES = page_configurations['categories'] #List of dictionaries
radioCategories = ['Home']
for i in CATEGORIES:
    radioCategories.append(i['name'])
selected_category_name = st.sidebar.radio('', radioCategories)

if selected_category_name == "Home" or selected_category_name not in radioCategories:
    defaultDisplayHome()

else:
    #perhaps put this into a 'displayOneCategory' function...
    category = getCategory(selected_category_name, CATEGORIES)
    DATASETS = category['datasets']
    radioDatasets = ['Home']
    for i in DATASETS:
        radioDatasets.append(i['datasetName'])
    datasetSelection = st.sidebar.radio('', radioDatasets)
    if datasetSelection == "Home" or datasetSelection not in radioDatasets:
        categoryDisplayHome()
    else:
        page = DatasetPageCreator(getDataset(datasetSelection, DATASETS))
        page.loadPage()

credit = "This project is supported by a UofU HCI CCPS pilot grant and by NSF Award IIS-1816149."
footer.footer(credit)
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
