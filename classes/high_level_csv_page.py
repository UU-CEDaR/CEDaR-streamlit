"""Dataset page
Create a web page for a dataset. """
import urllib

import pandas as pd
import streamlit as st
import yaml
from google.cloud import storage

from classes.data_filterer import (MultipleTextOptionsFilterer,
                                  NumericSliderFilterer)

from .VisualizationCreator import VisualizationCreator


class DatasetPageCreator:
    # pylint: disable=line-too-long, invalid-name, missing-function-docstring
    """A class used to store all dataset variables and to display them.
    This class also handles much of the functionality of the dataset, such as downloading
    csvs, data dictionaries, and filtering data.
    """

    def __init__(self, dataset):
        """
        When this class is given a dataset, it will configure all variables
            to be read later in loadpage()

        Args:
            dataset: A dataset part of the config YAML file.

        Returns:
            None

        """
        self.data_filterers = []
        self.setDatasetSummary(self.getFromDictOrDisplayWarning(dataset, 'summary'))
        self.setName(dataset.get('datasetName', None))
        year_numeric_slider_filterer = dataset.get('yearNumericSliderFilterer', None)
        self.year_range = None
        if year_numeric_slider_filterer is not None:
            self.year_range = str(self.getFromDictOrDisplayWarning(year_numeric_slider_filterer, 'min'))
            self.year_range += '-' + str(self.getFromDictOrDisplayWarning(year_numeric_slider_filterer, 'max'))
        self.setFileFormat(dataset.get('fileFormat', None))
        self.setOriginalDataSource(dataset.get('originalDataSource', None))
        self.setDataDictionaryAvailability(dataset.get('dataDictionaryAvailable', None))
        if self.dataDictionaryAvailable is not None:
            bucket = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryBucket')
            blob = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryBlob')
            dictionary_filename = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryFilename')
            mime = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryMime')
            self.setDataDictionaryCloudConfigurations(bucket, blob, dictionary_filename, mime)
        self.setVisualizationAvailable(dataset.get('visualizationAvailable', False))
        self.visualization = None
        if self.visual:
            f = urllib.request.urlopen(dataset.get('visualizationLink', None))
            page_configurations = yaml.safe_load(f.read())
            self.visualization = VisualizationCreator(page_configurations)
        if year_numeric_slider_filterer is not None:
            self.addNumericSliderFiltererIfValid(year_numeric_slider_filterer)
        numeric_slider_filterers = dataset.get('numericSliderFilterers', None)
        if numeric_slider_filterers is not None:
            for i in numeric_slider_filterers:
                self.addNumericSliderFiltererIfValid(i)
        multiple_text_slider_filterers = dataset.get('multipleTextOptionsFilterers', None)
        if multiple_text_slider_filterers is not None:
            for i in multiple_text_slider_filterers:
                self.addMultipleTextOptionsFilterer(i)
        self.setCSVDownloadLink(self.getFromDictOrDisplayWarning(dataset, 'csvDownloadLink'))
        self.setCSVFilename(self.getFromDictOrDisplayWarning(dataset, 'csvFileDownloadName'))
        self.data_dictionary_filename = None
        self.csv_file = None


    def getFromDictOrDisplayWarning(self, dataset, key):
        """
        Attempts to retrieve a variable from the dictionary, and if it doesn't exist, streamlit will display an error.

        Args:
            dataset: The dictionary that you are reading from.
            key: The key of the value that you are attempting to read from the dictionary.

        Returns:
            dataset[value] if dataset has `key`.
            `None` if dataset does not have `key`.

        """
        if key in dataset:
            return dataset[key]
        else:
            st.write("WARNING. Dataset is not initialized at required value " + key)
            return None

    def addNumericSliderFiltererIfValid(self, dataset):
        title = self.getFromDictOrDisplayWarning(dataset, 'title')
        minimal = self.getFromDictOrDisplayWarning(dataset, 'min')
        maximal = self.getFromDictOrDisplayWarning(dataset, 'max')
        columnName = self.getFromDictOrDisplayWarning(dataset, 'columnName')
        if title is None or minimal is None or maximal is None or columnName is None:
            return
        else:
            filterer = NumericSliderFilterer(title, minimal, maximal, columnName)
            self.addDataFilterer(filterer)

    def addMultipleTextOptionsFilterer(self, dataset):
        title = self.getFromDictOrDisplayWarning(dataset, 'title')
        allOptions = self.getFromDictOrDisplayWarning(dataset, 'allOptions')
        defaultOptions = self.getFromDictOrDisplayWarning(dataset, 'defaultOptions')
        columnName = self.getFromDictOrDisplayWarning(dataset, 'columnName')
        if title is None or allOptions is None or defaultOptions is None or columnName is None:
            return
        else:
            filterer = MultipleTextOptionsFilterer(title, allOptions, defaultOptions, columnName)
            self.addDataFilterer(filterer)



    #|Setter Functions|


    def setName(self, name):
        self.name = name

    def setDataDictionaryFileName(self, dataDictionaryFilename):
        self.data_dictionary_filename = dataDictionaryFilename

    def setOriginalDataSource(self, originalDataSource):
        self.originalDataSource = originalDataSource

    def setFileFormat(self, fileFormat):
        self.fileFormat = fileFormat

    def setDataDictionaryCloudConfigurations(self, bucket, blob, filename, mime):
        self.bucket = bucket
        self.blob = blob
        self.setDataDictionaryFileName(filename)
        self.mime = mime

    def setDataDictionaryAvailability(self, available):
        self.dataDictionaryAvailable = available

    def setVisualizationAvailable(self, visual):
        self.visual = visual

    def setDatasetSummary(self, info):
        self.info = info

    def addDataFilterer(self, dataFilterer):
        self.data_filterers.append(dataFilterer)

    def setCSVDownloadLink(self, csvDownloadLink):
        self.csvDownloadLink = csvDownloadLink

    def setCSVFilename(self, csvFilename):
        self.csvFilename = csvFilename





    def loadPage(self):
        """
        Displays all the data previously created from the yaml file on the website.

        Args:
            None.

        Returns:
            None.

        """
        if self.name is not None:
            st.write("## " + str(self.name))
        if self.info is not None:
            st.write(str(self.info))
        if self.year_range is not None:
            st.write("Years Available: " + str(self.year_range))
        if self.originalDataSource is not None:
            st.write("Data Source: " + str(self.originalDataSource))
        if self.fileFormat is not None:
            st.write("Data format: " + self.fileFormat)

        if self.dataDictionaryAvailable is not None:
            if self.dataDictionaryAvailable:
                st.write("Metadata is available for this dataset")
            else:
                st.write("Metadata is not available for this dataset")
        if self.bucket is not None and self.blob is not None and self.data_dictionary_filename is not None:
            placeholder = st.empty()
            placeholder.text("Initializing metadata download...")
            st.download_button("Download Metadata", self.onClickDownloadDataDictionary(), file_name=self.data_dictionary_filename, mime=self.mime)
            placeholder.empty()

        if self.visual is not None:
            st.write("Visualization source: " + str(self.visual))
        else:
            st.write("Visualization is not available for this dataset")
        if self.visualization is not None:
            self.visualization.createMap()
        for filterer in self.data_filterers:
            filterer.displayThings()

        if self.csvDownloadLink is not None:
            if st.button('Apply filters to dataset'):
                placeholder = st.empty()
                placeholder.text("Preparing CSV download...")
                self.csv_file = self.onClickDownloadCsv()
                placeholder.empty()
                st.download_button("Download CSV", self.csv_file, file_name=self.csvFilename, mime='text/csv')


    #|Helper Functions for loading the page|


    @st.cache
    def onClickDownloadDataDictionary(self):
        """
        Downloads the data dictionary from the google cloud repository.

        Args:
            None

        Returns:
            the file in bytes that you downloaded from the google cloud

        """
        storage_client = storage.Client.create_anonymous_client()
        bucket = storage_client.bucket(self.bucket)
        blob = bucket.blob(self.blob)

        blob.download_to_filename(self.data_dictionary_filename)
        download = blob.download_as_bytes()

        return download

    @st.cache
    def onClickDownloadCsv(self):
        """
        Downloads the csv from google cloud and edits it using the Data Filterers.

        Args:
            None

        Returns:
            the filtered .csv in bytes.

        """
        df = pd.read_csv(self.csvDownloadLink)
        for filterer in self.data_filterers:
            df = filterer.filterCSV(df)
        finalCSV = df.to_csv(index=False)
        return finalCSV
        