import streamlit as st
import folium
import matplotlib as plt
import branca.colormap as colormap
from streamlit_folium import folium_static
import xarray as xr
import numpy as np
import geopandas
import pandas as pd

class VisualizationCreator:
	
	"""
    Sets the dictionary that your visualization is being created from.

	Args:
		dataset: The dictionary of the visualization.

	Returns:
		None
	"""
	def __init__(self, dataset):
		self.dataset = dataset
		
		

	"""
    Initializes the values of the map and displays it on the screen based on the presets given.
		Note that the Chloropleth creation of the map is not finished, but the child creation
		of the map is at least configured for acag.py.

	Args:
		None

	Returns:
		None
	"""
	def createMap(self):
		psbSelectboxName, psbOptions = self.getPollutantSelectbox(self.dataset)
		pollutant = st.selectbox(psbSelectboxName, psbOptions)
		csbSelectboxName, csbOptions = self.getCompositionSelectbox(self.dataset)
		comp = st.selectbox(csbSelectboxName, csbOptions)
		datasetValue = self.getDatasetBasedOnPollutantProvided(self.dataset, pollutant)
		year = self.createCompositionSlider(comp, datasetValue)
		sourceFileInfo = self.dataset["sourceFile"]

		if sourceFileInfo["mapType"] == "Chloropleth":
			pass
			#self.load_chloropleth()
		if sourceFileInfo["mapType"] == "child":
			self.load_child(pollutant, year, sourceFileInfo)
		
		
#######################################################################################

	"""
    Gets the name and all the possible selections of the pollutant datasets.

	Args:
		dataset: The dataset with the pollutant data

	Returns:
		The title of the pollutant datasets, as well as all of the possible selections for pollutants.

	"""
	def getPollutantSelectbox(self, dataset):
		csbSelectboxName = dataset['PollutantDatasets']['PollutantDatasetTitle']
		csbOptions = []
		for i in dataset['PollutantDatasets']['Pollutants']:
			csbOptions.append(i['selectionName'])
		return csbSelectboxName, csbOptions
		
	
	def getCompositionSelectbox(self, dataset):
		"""
		Gets the name and all the possible selections of the composition datasets.

		Args:
			dataset: The dataset with the composition data

		Returns:
			The title of the composition datasets, as well as all of the possible selections for compositions.
			
		"""
		psbSelectboxName = dataset['CompositionDatasets']['CompositionDatasetTitle']
		psbOptions = []
		for i in dataset['CompositionDatasets']['Selections']:
			psbOptions.append(i['selectionName'])
		return psbSelectboxName, psbOptions
		
	
	def createCompositionSlider(self, comp, dataset):
		"""
		Creates a slider and sets the year that the user selected.

		Args:
			comp: The selected composition for the slider.
			dataset: The dataset of the currently selected pollutant.

		Returns:
			The year that the use selected for the dataset.
			
		"""
		year = st.slider(
			comp,
			dataset['min'],
			dataset['max'],
			dataset['max']
		)
		return year
		
	def getDatasetBasedOnPollutantProvided(self, dataset, pollutant):
		"""
		Gets the pollutant dataset based on the 

		Args:
			comp: The selected composition for the slider.
			dataset: The dataset of the currently selected pollutant.

		Returns:
			The year that the use selected for the dataset.
			
		"""
		for i in dataset['PollutantDatasets']['Pollutants']:
			if (i['selectionName'] == pollutant):
				return i
		return None



#########################################################################################

	def load_child(self, pollutant, year, filename):
		self.image, self.min, self.max, self.caption = self.load_data_child(pollutant, year, filename)
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

		
	@st.cache
	def load_data_child(self, comp, year, sourceFile):
		if (sourceFile["fileType"] == "zarr"):
			return self.load_zarr_child(comp, year, sourceFile["fileName"])
		if (sourceFile["fileType"] == "shp"):
			return self.load_shp_child(comp, year, sourceFile["fileName"])
		else: #Do more later.
			return None

	@st.cache
	def load_zarr_child(self, comp, year, filename):
		ds = xr.open_zarr(filename) #how to get file name?
		caption = f'{ds[comp].standard_name} ({ds[comp].units})'
		data = ds[comp].loc[f"{year}-01-01"].data
		min, max = data.min(), data.max()
		data = (data - data.min()) / (data.max() - data.min()) # normalize
		cm = plt.cm.get_cmap('viridis_r')
		return cm(data), min, max, caption

	@st.cache
	def load_shp_child(self, comp, year, sourceFile):
		pass


###########################################################################################
	
	@st.cache
	def load_chloropleth(self, gdfFilename, dfFilename, chloropleth, comp, year):
		df, gdf = self.load_shp_child(gdfFilename, dfFilename, comp, year)
		m = folium.Map(location=[39.6, -111.5],
                   min_zoom=6, max_zoom=12, zoom_start=7)
		# folium.GeoJson(data=gdf["geometry"]).add_to(m)
		folium.Choropleth(
			geo_data=gdf,
			data=df,
			columns=["fips", "pred_wght"],
			key_on='feature.properties.GEOID10',
			fill_color="OrRd",
			nan_fill_color='red',
			fill_opacity=0.7,
			line_opacity=0.2,
			legend_name=CAPTION[comp],
		).add_to(m)
		# call to render Folium map in Streamlit
		folium_static(m, width=700, height=800)

	@st.cache
	def load_shp_child(self, gdfFilename, dfFilename, year, comp):
		gdf = geopandas.read_file(gdfFilename, dfFilename)
		gdf = gdf[['GEOID10','NAMELSAD10','geometry']]
		df = pd.read_csv(dfFilename)
		df = df[(df.year==year) & (df.pollutant==comp)][['fips','pred_wght']].astype({'fips':'str'})	
		