"""Create a web page for a category."""
import pkgutil

import streamlit as st


class category_class:
    # pylint: disable=missing-class-docstring, invalid-name, missing-function-docstring

    def __init__(self, name=None, description=None, path=None):
        self.setName(name)
        self.setDescription(description)
        self.setPackagePath(path)

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setPackagePath(self, path):
        self.packagePath = path

    def getDatasets(self):
        theList = ['Description']
        for _, name, _ in pkgutil.iter_modules([self.packagePath]):
            theList.append(name)
        return theList

    def page(self):
        st.write("## " + self.name)
        st.write(self.description)
        DATASETS = self.getDatasets()
        st.sidebar.title('DATASETS')
        selection = st.sidebar.radio('', DATASETS)

        params = st.experimental_get_query_params()

        if selection != "Home":
            st.experimental_set_query_params (
                category=params["category"][0],
                dataset = selection
            )
        else:
            st.experimental_set_query_params(
                category=params["category"][0]
            )
