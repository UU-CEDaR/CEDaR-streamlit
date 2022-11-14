import streamlit as st
from google.cloud import storage
from io import StringIO
import pandas as pd
import numpy as np
from zmq import VMCI_BUFFER_SIZE
from classes.VisualizationCreator import VisualizationCreator
from classes.DataFilterer import NumericSliderFilterer
from classes.DataFilterer import MultipleTextOptionsFilterer
import urllib
import yaml

"""
DatasetPageCreator: A class used to store all dataset variables and to display them.
This class also handles much of the functionality of the dataset, such as downloading
csvs, data dictionaries, and filtering data.
"""
class DatasetPageCreator:


    
    def __init__(self, dataset):
        """
        When this class is given a dataset, it will configure all variables 
            to be read later in loadpage()

        Args:
            dataset: A dataset part of the config YAML file.

        Returns:
            None

        """
        self.dataFilterers = []
        self.setDatasetSummary(self.getFromDictOrDisplayWarning(dataset, 'summary'))
        self.setName(dataset.get('datasetName', None))
        yearNumericSliderFilterer = dataset.get('yearNumericSliderFilterer', None)
        self.yearRange = None
        if (yearNumericSliderFilterer is not None):
            self.setYearRange(str(self.getFromDictOrDisplayWarning(yearNumericSliderFilterer, 'min')) + '-' + str(self.getFromDictOrDisplayWarning(yearNumericSliderFilterer, 'max')))
        self.setFileFormat(dataset.get('fileFormat', None))
        self.setOriginalDataSource(dataset.get('originalDataSource', None))
        self.setDataDictionaryAvailability(dataset.get('dataDictionaryAvailable', None))
        if self.dataDictionaryAvailable is not None:
            bucket = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryBucket')
            blob = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryBlob')
            dictionaryFilename = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryFilename')
            mime = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryMime')
            self.setDataDictionaryCloudConfigurations(bucket, blob, dictionaryFilename, mime)
        self.setVisualizationAvailable(dataset.get('visualizationAvailable', False))
        self.visualization = None
        if (self.visual):
            f = urllib.request.urlopen(dataset.get('visualizationLink', None))
            page_configurations = yaml.safe_load(f.read()) 
            self.visualization = VisualizationCreator(page_configurations)
        if yearNumericSliderFilterer is not None:
            self.addNumericSliderFiltererIfValid(yearNumericSliderFilterer)
        numericSliderFilterers = dataset.get('numericSliderFilterers', None)
        if numericSliderFilterers is not None:
            for i in numericSliderFilterers:
                self.addNumericSliderFiltererIfValid(i)
        multipleTextSliderFilterers = dataset.get('multipleTextOptionsFilterers', None)
        if multipleTextSliderFilterers is not None:
            for i in multipleTextSliderFilterers:
                self.addMultipleTextOptionsFilterer(i)
        self.setCSVDownloadLink(self.getFromDictOrDisplayWarning(dataset, 'csvDownloadLink'))
        self.setCSVFilename(self.getFromDictOrDisplayWarning(dataset, 'csvFileDownloadName'))



    def getFromDictOrDisplayWarning(self, dict, value):
        """
        Attempts to retrieve a variable from the dictionary, and if it doesn't exist, streamlit will display an error.

        Args:
            dict: The dictionary that you are reading from.
            value: The value that you are attempting to read from the dictionary.

        Returns:
            dict[value] if value is a key in dict.
            '' if value is not a key in dict.

        """
        try:
            result = dict[value]
            return result
        except:
            st.write("WARNING. Dataset is not initialized at required value " + value)
            return ''

    def addNumericSliderFiltererIfValid(self, dataset):
        title = self.getFromDictOrDisplayWarning(dataset, 'title')
        min = self.getFromDictOrDisplayWarning(dataset, 'min')
        max = self.getFromDictOrDisplayWarning(dataset, 'max')
        columnName = self.getFromDictOrDisplayWarning(dataset, 'columnName')
        if title is None or min is None or max is None or columnName is None:
            return
        else:
            filterer = NumericSliderFilterer(title, min, max, columnName)
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
        self.dataDictionaryFilename = dataDictionaryFilename

    def setYearRange(self, yearRange):
        self.yearRange = yearRange
    
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
        self.dataFilterers.append(dataFilterer)

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
        if (self.name is not None):
            st.write("## " + str(self.name))
        if (self.info is not None):
            st.write(str(self.info))
        if (self.yearRange is not None):
            st.write("Years Available: " + str(self.yearRange))
        if (self.originalDataSource is not None):
            st.write("Data Source: " + str(self.originalDataSource))
        if (self.fileFormat is not None):
            st.write("Data format: " + self.fileFormat)
        
        if (self.dataDictionaryAvailable is not None):
            if (self.dataDictionaryAvailable):
                st.write("Metadata is available for this dataset")
            else:
                st.write("Metadata is not available for this dataset")
        if (self.bucket is not None and self.blob is not None and self.dataDictionaryFilename is not None):
            placeholder = st.empty()
            placeholder.text("Initializing metadata download...")
            st.download_button("Download Metadata", self.onClickDownloadDataDictionary(), file_name=self.dataDictionaryFilename, mime=self.mime)
            placeholder.empty()
        
        if (self.visual is not None):
            st.write("Visualization source: " + str(self.visual))
        else:
            st.write("Visualization is not available for this dataset")
        if self.visualization is not None:
                self.visualization.createMap()
        for filterer in self.dataFilterers:
            filterer.displayThings()
        
        if (self.csvDownloadLink is not None):
            if st.button('Apply filters to dataset'):
                placeholder = st.empty()
                placeholder.text("Preparing CSV download...")
                self.csvFile = self.onClickDownloadCsv()
                placeholder.empty()
                st.download_button("Download CSV", self.csvFile, file_name=self.csvFilename, mime='text/csv')
        
            

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

        blob.download_to_filename(self.dataDictionaryFilename)
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
        for filterer in self.dataFilterers:
            df = filterer.filterCSV(df)
        finalCSV = df.to_csv(index=False)
        return finalCSV

        
        