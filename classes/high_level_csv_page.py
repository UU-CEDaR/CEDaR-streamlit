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



#This class creates a page from a YAML file based on the information given.
class DatasetPageCreator:

#|Main Function|
    def __init__(self, dataset):
        #The data filterers that will be used to filter the .csv file. See DataFilterer.py for more info on that.
        self.dataFilterers = []
        #Sets the summary of the dataset at the top of the page.
        self.setDatasetSummary(self.getFromDictOrDisplayWarning(dataset, 'summary'))
        #Sets the name of the dataset based on the "datasetName" variable in the YML file.
        self.setName(dataset.get('datasetName', None))
        #Gets the yearNumericSliderFilterer from the dataset.
        yearNumericSliderFilterer = dataset.get('yearNumericSliderFilterer', None)
        self.yearRange = None
        #If the yearNumericSliderFilterer is not none, then display the min and max set in the filterer.
        if (yearNumericSliderFilterer is not None):
            self.setYearRange(str(self.getFromDictOrDisplayWarning(yearNumericSliderFilterer, 'min')) + '-' + str(self.getFromDictOrDisplayWarning(yearNumericSliderFilterer, 'max')))
        #Sets the file format. This supports ".csv" and ".shp" right now.
        self.setFileFormat(dataset.get('fileFormat', None))
        #Gets the link to the site where the original data came from.
        self.setOriginalDataSource(dataset.get('originalDataSource', None))
        #Sets a bool (true/false) if there is a data dictionary available.
        self.setDataDictionaryAvailability(dataset.get('dataDictionaryAvailable', None))
        #If the data dictionary is available, set the link to it from google drive.
        if self.dataDictionaryAvailable is not None:
            #The google drive bucket you are pulling from. this will be "cedar-datasets".
            bucket = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryBucket')
            #The location of the file based on the bucket. Look up blobs on google cloud or cedar_config.yml for more information.
            blob = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryBlob')
            #The name of the file that you wish to download from the bucket.
            dictionaryFilename = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryFilename')
            #The MIME of the file, or configurations needed to encode the file.
            mime = self.getFromDictOrDisplayWarning(dataset, 'dataDictionaryMime')
            #sets the download location of the data dictionary.
            self.setCloudConfigurations(bucket, blob, dictionaryFilename, mime)
        #Gets if the visualization is available or not.
        self.setVisualizationAvailable(dataset.get('visualizationAvailable', False))
        #The variable used to represent visualizations.
        self.visualization = None
        if (self.visual):
            #Gets the link to the visualization from google cloud.
            f = urllib.request.urlopen(dataset.get('visualizationLink', None))
            #Gets the information of the visualization from the yml file.
            page_configurations = yaml.safe_load(f.read()) 
            #Creates the visualization creator based on the page configurations.
            self.visualization = VisualizationCreator(page_configurations)
        if yearNumericSliderFilterer is not None:
            #Creates a numeric slider filterer that filters the years of the dataset.
            self.addNumericSliderFiltererIfValid(yearNumericSliderFilterer)
        #Create every numeric slider filterer that was listed in the .yml file.
        numericSliderFilterers = dataset.get('numericSliderFilterers', None)
        if numericSliderFilterers is not None:
            for i in numericSliderFilterers:
                self.addNumericSliderFiltererIfValid(i)
        #Create every multiple text slider filterer that was listed in the .yml file.
        multipleTextSliderFilterers = dataset.get('multipleTextOptionsFilterers', None)
        if multipleTextSliderFilterers is not None:
            for i in multipleTextSliderFilterers:
                self.addMultipleTextOptionsFilterer(i)
        #Gets the csv download link from the yml file.
        self.setCSVDownloadLink(self.getFromDictOrDisplayWarning(dataset, 'csvDownloadLink'))
        #Sets the csv file name from the yml file.
        self.setCSVFilename(self.getFromDictOrDisplayWarning(dataset, 'csvFileDownloadName'))


#|Convenience Functions called in the Main Function|
    def getFromDictOrDisplayWarning(self, dict, value):
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


    #Sets the name of the dataset.
    def setName(self, name):
        self.name = name
 
    #Sets the name of the Data Dictionary.
    def setDataDictionaryFileName(self, dataDictionaryFilename):
        self.dataDictionaryFilename = dataDictionaryFilename

    #Sets the year range (as a string) for the dataset
    def setYearRange(self, yearRange):
        self.yearRange = yearRange
    
    #Sets the original data source of the data.
    def setOriginalDataSource(self, originalDataSource):
        self.originalDataSource = originalDataSource

    #Sets the file format of the data to be .csv, .shp, etc.
    def setFileFormat(self, fileFormat):
        self.fileFormat = fileFormat

    #Sets the configurations of the cloud.
    def setCloudConfigurations(self, bucket, blob, filename, mime):
        self.bucket = bucket
        self.blob = blob
        self.setDataDictionaryFileName(filename)
        self.mime = mime

    #Sets true/false if the data dictionary is available.
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



#|Main function that loads the page|

    def loadPage(self):
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
        storage_client = storage.Client.create_anonymous_client()
        bucket = storage_client.bucket(self.bucket)
        blob = bucket.blob(self.blob)

        blob.download_to_filename(self.dataDictionaryFilename)
        download = blob.download_as_bytes()
        
        return download

    @st.cache
    def onClickDownloadCsv(self):
        
        df = pd.read_csv(self.csvDownloadLink)
        for filterer in self.dataFilterers:
            df = filterer.filterCSV(df)
        finalCSV = df.to_csv(index=False)
        return finalCSV

    @st.cache
    def editCSV(self, download):
        for dataFilterer in self.dataFilterers:
            download = dataFilterer.filterCSV(download)
        return download
        
        