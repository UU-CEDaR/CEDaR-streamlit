import streamlit as st
from google.cloud import storage
from io import StringIO
import pandas as pd
import numpy as np

class high_level_csv_page:

        def __init__(self, name = None, year = None, source = None, filename = None, mime = "application/zip",
            dataType = None, bucket_name = None, blob_name = None, available = None, info = None,
            visualization = None, dataFilterers = None, csvDownloadLink = None, csvFileName = None):
            self.setName(name)
            self.setYear(year)
            self.setSource(source)
            self.setDataType(dataType)
            self.setCloudConfigurations(bucket_name, blob_name, filename, mime)
            self.setMetadataAvailability(available)
            self.setVisualization(visualization)
            self.setAdditionalInformation(info)
            self.dataFilterers = []
            self.setCSVDownloadLink(csvDownloadLink)
            self.setCSVFilename(csvFileName)

        def setName(self, name):
            self.name = name

        def setFileName(self, filename):
            self.filename = filename

        def setYear(self, year):
            self.year = year
        
        def setSource(self, source):
            self.source = source

        def setDataType(self, dataType):
            self.dataType = dataType

        def setCloudConfigurations(self, bucket, blob, filename, mime):
            self.bucket = bucket
            self.blob = blob
            self.setFileName(filename)
            self.mime = mime

        def setMetadataAvailability(self, available):
            self.metadataAvailabile = available

        def setVisualization(self, visual):
            self.visual = visual

        def setAdditionalInformation(self, info):
            self.info = info

        def addDataFilterer(self, dataFilterer):
            self.dataFilterers.append(dataFilterer)

        def setCSVDownloadLink(self, csvDownloadLink):
            self.csvDownloadLink = csvDownloadLink

        def setCSVFilename(self, csvFilename):
            self.csvFilename = csvFilename


        @st.cache
        def onClickDownloadLink(self):
            storage_client = storage.Client.create_anonymous_client()
            bucket = storage_client.bucket(self.bucket)
            blob = bucket.blob(self.blob)

            blob.download_to_filename(self.filename)
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


        def loadPage(self):
            if (self.name is not None):
                st.write("## " + str(self.name))
            if (self.info is not None):
                st.write(str(self.info))
            if (self.year is not None):
                st.write("Years Available: " + str(self.year))
            if (self.source is not None):
                st.write("Data Source: " + str(self.source))
            if (self.dataType is not None):
                st.write("Data format: " + self.dataType)
            
            if (self.metadataAvailabile is not None):
                if (self.metadataAvailabile):
                    st.write("Metadata is available for this dataset")
                else:
                    st.write("Metadata is not available for this dataset")
            if (self.bucket is not None and self.blob is not None and self.filename is not None):
                placeholder = st.empty()
                placeholder.text("Initializing metadata download...")
                st.download_button("Download Metadata", self.onClickDownloadLink(), file_name=self.filename, mime=self.mime)
                placeholder.empty()
           
            if (self.visual is not None):
                st.write("Visualization source: " + str(self.visual))
            else:
                st.write("Visualization is not available for this dataset")
            st.write("IF VISUALIZATION WAS AVAILABLE, THIS IS WHERE IT WOULD GO")
            for filterer in self.dataFilterers:
                filterer.displayThings()
            
            if (self.csvDownloadLink is not None):
                if st.button('Apply filters to dataset'):
                    placeholder = st.empty()
                    placeholder.text("Preparing CSV download...")
                    self.csvFile = self.onClickDownloadCsv()
                    placeholder.empty()
                    st.download_button("Download CSV", self.csvFile, file_name=self.csvFilename, mime='text/csv')
            
                

            
            