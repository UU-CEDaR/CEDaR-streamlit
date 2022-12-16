"""These classes create widgets that filter csvs."""
import streamlit as st


# pylint: disable=invalid-name, missing-class-docstring, missing-function-docstring, invalid-name
class DataFilterer:
    def displayThings(self):
        pass

    def filterCSV(self, df):
        pass


class NumericSliderFilterer(DataFilterer):
    """Creates a slider widget that filters a csv by range.
    """

    def __init__(self, title, min_value, max_value, csvColumnName):
        """
        Initializes a numeric slider filterer with
        a short title, a minimum value, a maximum value,
        and the column that you need to filter out.

        Args:
            title: The title of the numeric slider filterer.
            min: The minimum value of the csvColumnName.
            max: The maximum value of the csvColumnName.
            csvColumnName: The name of the column that you are filtering.

        Returns:
            None
        """
        self.title = title
        self.min = min_value
        self.max = max_value
        self.csvColumnName = csvColumnName
        self.slider = None

    def displayThings(self):
        """
        Displays the slider widget on screen.

        Args:
            None

        Returns:
            None
        """
        self.slider = st.slider(
            self.title,
            min_value = self.min,
            max_value = self.max,
            value = (self.min, self.max)
        )


    def filterCSV(self, df):
        """
        Filters the dataframe to have values between 0 and 1
        on column name csvColumnName.

        Args:
            df: The df derived from the .csv that you are filtering.

        Returns:
            the filtered dataframe.
        """
        df = df.loc[(df[self.csvColumnName] >= self.slider[0])]
        df = df[df[self.csvColumnName] <= self.slider[1]]
        return df


class MultipleTextOptionsFilterer(DataFilterer):
    """
    Code for a widget to filter out a csv based on
    selected values.
    """

    def __init__(self, title, allOptions, someOptions, csvColumnName):
        """
        Initializes the values of the data filterer.

        Args:
            title: The title of the MultipleTextOptionFilterer
            allOptions: All of the possible options of csvColumnName.
            someOptions: The default options of csvColumnName.
            csvColumnName: The csv column name that you are filtering on.

        Returns:
            None
        """
        self.title = title
        self.allOptions = allOptions
        self.someOptions = someOptions
        self.csvColumnName = csvColumnName
        self.multiselect = None

    def displayThings(self):
        """
        Displays the slider widget on screen.

        Args:
            None

        Returns:
            None
        """
        self.multiselect = st.multiselect(
            self.title,
            self.allOptions,
            self.someOptions
        )
        if st.button("Select all options"):
            self.multiselect = self.allOptions

    #Filters the csv to only have rows where columnName is in the columns selected.
    def filterCSV(self, df):
        return df[df[self.csvColumnName].isin(self.multiselect)]
