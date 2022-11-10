import streamlit as st
import folium
import matplotlib as plt
import branca.colormap as colormap
from streamlit_folium import folium_static
import xarray as xr
import numpy as np

class VisualizationCreator:
	
	def __init__(self, dataset):
		self.dataset = dataset
		
		

	def createMap(self):
		psbSelectboxName, psbOptions = self.getPollutantSelectbox(self.dataset)
		pollutant = st.selectbox(psbSelectboxName, psbOptions)
		csbSelectboxName, csbOptions = self.getCompositionSelectbox(self.dataset)
		comp = st.selectbox(csbSelectboxName, csbOptions)
		datasetValue = self.getDatasetBasedOnYearProvided(self.dataset, pollutant)
		year = self.createCompositionSlider(comp, datasetValue)
		filename = self.dataset["sourceFile"]
		self.image, self.min, self.max, self.caption = self.load_data(pollutant, year, filename)
		self.foliumMapValues = self.dataset["folium_map"]
		m = folium.Map(location = [self.foliumMapValues["latitude"], self.foliumMapValues["longitude"]],
					min_zoom=self.foliumMapValues["min_zoom"], max_zoom=self.foliumMapValues["max_zoom"],
					zoom_start=self.foliumMapValues["zoom_start"])
		
		fc = self.dataset["folium_child"]
		m.add_child(folium.raster_layers.ImageOverlay(self.image,
					opacity = fc["opacity"], mercator_project = fc["mercator_project"],
					bounds = [[fc["minLatitude"], fc["minLongitude"]], [fc["maxLatitude"], fc["maxLongitude"]]]))
		cm = plt.cm.get_cmap('viridis_r')	
		color_list = [cm(i) for i in np.linspace(0, 1, num=10)]
		legend = colormap.LinearColormap(color_list, caption=self.caption).scale(vmin=self.min, vmax=self.max)
		m.add_child(legend)
		folium_static(m, width=700, height=800)
		
	
	def getPollutantSelectbox(self, dataset):
		csbSelectboxName = dataset['PollutantDatasets']['PollutantDatasetTitle']
		csbOptions = []
		for i in dataset['PollutantDatasets']['Pollutants']:
			csbOptions.append(i['selectionName'])
		return csbSelectboxName, csbOptions
		
	def getCompositionSelectbox(self, dataset):
		psbSelectboxName = dataset['CompositionDatasets']['CompositionDatasetTitle']
		psbOptions = []
		for i in dataset['CompositionDatasets']['Selections']:
			psbOptions.append(i['selectionName'])
		return psbSelectboxName, psbOptions
		
	def createCompositionSlider(self, comp, dataset):
		year = st.slider(
			comp,
			dataset['min'],
			dataset['max'],
			dataset['max']
		)
		return year
		
	def getDatasetBasedOnYearProvided(self, dataset, comp):
		for i in dataset['PollutantDatasets']['Pollutants']:
			if (i['selectionName'] == comp):
				return i
		return None
		
	@st.cache
	def load_zarr(self, comp, year, filename):
		ds = xr.open_zarr(filename) #how to get file name?
		caption = f'{ds[comp].standard_name} ({ds[comp].units})'
		data = ds[comp].loc[f"{year}-01-01"].data
		min, max = data.min(), data.max()
		data = (data - data.min()) / (data.max() - data.min()) # normalize
		cm = plt.cm.get_cmap('viridis_r')
		return cm(data), min, max, caption
		
		
	@st.cache
	def load_data(self, comp, year, sourceFile):
		if (sourceFile["fileType"] == "zarr"):
			return self.load_zarr(comp, year, sourceFile["fileName"])
		else: #Do more later.
			return None
	
	
	@st.cache
	def load_zarr(self, comp, year, sourceFile):
		ds = xr.open_zarr(sourceFile)
		caption = f'{ds[comp].standard_name} ({ds[comp].units})'
		data = ds[comp].loc[f"{year}-01-01"].data
		min, max = data.min(), data.max()
		data = (data - data.min()) / (data.max() - data.min()) # normalize
		cm = plt.cm.get_cmap('viridis_r')
		return cm(data), min, max, caption

