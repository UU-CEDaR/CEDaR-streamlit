import streamlit as st
import pandas as pd

#An object that the user will interact with that will filter the .csv
#somehow.
class DataFilterer:
    def displayThings(self):
        pass

    def filterCSV(self, df):
        pass


#Creates a slider to filter the .csv where csvColumnName is between min and max.
class NumericSliderFilterer(DataFilterer):
    #Title: The title of the numeric slider filterer.
    #Min: The minimum value that csvColumnName can possibly be.
    #Max: The maximum value that csvColumnName can possibly be.
    #CsvColumnName: The column in the csv that you are filtering for.
    def __init__(self, title, min, max, csvColumnName):
        self.title = title
        self.min = min
        self.max = max
        self.csvColumnName = csvColumnName

    def displayThings(self):
        self.slider = st.slider(
            self.title, 
            min_value = self.min,
            max_value = self.max,
            value = (self.min, self.max)
        )

    #Filters the csv where columnName is between the slided set values
    #of Min and Max.
    def filterCSV(self, df):
        df = df.loc[(df[self.csvColumnName] >= self.slider[0])]
        df = df[df[self.csvColumnName] <= self.slider[1]]
        return df


class MultipleTextOptionsFilterer(DataFilterer):
    #Title: The title of the multiple text options filterer.
    #allOptions: All the options that are available in the multiple text 
    #   options filterer.
    #someOptions: The default options that are available in the multiple text
    #   options filterer.
    #CsvColumnName: The column in the csv that you are filtering for.
    #There might be a way to get the selectable options more automatically.
    def __init__(self, title, allOptions, someOptions, csvColumnName):
        self.title = title
        self.allOptions = allOptions
        self.someOptions = someOptions
        self.csvColumnName = csvColumnName

    #Creates a multiselect with a tile and options.
    def displayThings(self):
        self.multiselect = st.multiselect(
            self.title,
            self.allOptions,
            self.someOptions
        )
        if st.button("Select all options"):
            self.multiselect = self.allOptions
    
    #Filters the csv to have a number of values in the multiSelect.
    def filterCSV(self, df):
        return df[df[self.csvColumnName].isin(self.multiselect)]