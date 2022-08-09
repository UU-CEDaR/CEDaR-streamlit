import streamlit as st
import pandas as pd

class DataFilterer:
    def displayThings(self):
        pass

    def filterCSV(self, df):
        pass


class NumericSliderFilterer(DataFilterer):
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


    def filterCSV(self, df):
        df = df.loc[(df[self.csvColumnName] >= self.slider[0])]
        df = df[df[self.csvColumnName] <= self.slider[1]]
        return df


class MultipleTextOptionsFilterer(DataFilterer):
    def __init__(self, title, allOptions, someOptions, csvColumnName):
        self.title = title
        self.allOptions = allOptions
        self.someOptions = someOptions
        self.csvColumnName = csvColumnName

    def displayThings(self):
        self.multiselect = st.multiselect(
            self.title,
            self.allOptions,
            self.someOptions
        )
        if st.button("Select all options"):
            self.multiselect = self.allOptions
    
    def filterCSV(self, df):
        return df[df[self.csvColumnName].isin(self.multiselect)]