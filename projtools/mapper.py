import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class Mapper:
    def __init__(self, df: pd.DataFrame, variable: str, on: ['borough', 'ward_name'], title: str, caption: str):
        """Maps a dataframe to a map of London either by borough or ward_name.

        Args:
            df (pd.DataFrame): dataframe to map
            variable (str): column name of variable to map
            on (borough', 'ward_name'): level to map on
            title (str): title of map
            caption (str): caption of map
        """
        base = Path(__file__).parent.parent

        # load the map data
        self.df = df
        self.variable = variable
        self.on = on
        self.title = title
        self.caption = caption

        # set up the map dataframe
        self.mapdf = gpd.read_file(base / "mapshapes/London_Ward.shp").rename(columns={'NAME': 'ward_name', 'DISTRICT': 'borough'})
        # standardising borough names
        self.mapdf['borough'] = self.mapdf['borough'].replace('City of Westminster', 'Westminster')

        # create the map
        self.make_map()

    def make_map(self):

        vmin, vmax = self.df[self.variable].min(), self.df[self.variable].max()
        fig, ax = plt.subplots(1, figsize=(10, 6))

        # merging the dataframes
        merged = self.mapdf.merge(self.df, left_on=self.on, right_index=True)

        # plotting the map
        merged.plot(column=self.variable, cmap='Blues', linewidth=0.8, ax=ax)

        ax.axis('off')
        sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm._A = []
        # cbar = fig.colorbar(sm)

        ax.set_title(
            self.title,
            fontdict={'fontsize': '25', 'fontweight': '3'}
        )
        ax.annotate(
            self.caption,
            xy=(0.1, .08),
            xycoords='figure fraction',
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=12,
            color='#555555'
        )