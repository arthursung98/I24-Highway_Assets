# Pacakge Imports
from utils import *
import importlib
import utils
importlib.reload(utils)
import os.path
from os import path
import matplotlib.pyplot as plt
import math
import pandas as pd

class Visualization :
    def __init__(self) :
        """ Constructor. Creates a path to the Maxtrix Asset file for visualization functions to use. """
        
        file_path = pathlib.Path().absolute().joinpath('../QGIS/MileMarker/Matrix Files')
        self.file_name = file_path.joinpath('total_asset_matrix.csv')
        
    def plot_graph(self, start_loc, end_loc) :
        """ Creates a visual representation graph of all assets on the highway.
    
        Args :
            start_loc : Starting point of the graph. Any number from 0 ~ 30.
            end_loc : Ending point of the graph. Any number from 0 ~ 30.
        """
        df = read_data(self.file_name, start_loc, end_loc)
        
        fig, ax = plt.subplots(figsize=(15,2))
        plt.xlim(start_loc + 52, end_loc + 52)
        plt.ylim(0, 120)
        ax.set_facecolor('grey')
        ax.axhline(y=60, color='yellow')
        
        rds_x, rds_y = get_asset_xy_coords(df, 'rds')
        dms_x, dms_y = get_asset_xy_coords(df, 'dms')
        cctv_x, cctv_y = get_asset_xy_coords(df, 'cctv')
        rds = plt.scatter(rds_x, rds_y, color='red', label='RDS')
        dms = plt.scatter(dms_x, dms_y, color='green', label='DMS')
        cctv = plt.scatter(cctv_x, cctv_y, color='yellow', label='CCTV')

        plt.title(f'Assets from Miles {start_loc+52} to {end_loc+52}', fontdict={'fontsize':'large','fontweight':'bold'}, pad=20)
        plt.legend(loc='upper center', bbox_to_anchor=(1, 1.55), fancybox=True, shadow=True, ncol=1)
        plt.xlabel('Miles')
        plt.ylabel('ft')
        plt.savefig('../Output Graphs/asset_graph.jpg', bbox_inches='tight')
        
        
def read_data(file_name, start_loc, end_loc) :
    """ Reads the Matrix CSV file and querys only the assets that are within the given range.
    
    Args :
        file_name : The location / name of the Matrix CSV file.
        start_loc : Starting point of the query. Any number from 0 ~ 30.
        end_loc : Ending point of the query. Any number from 0 ~ 30.
        
    Return :
        The queryed DataFrame.
    """
    df = pd.read_csv(file_name, skiprows=0, error_bad_lines=False, index_col=False)
    df = df.query('Direction != "other"')
    df = df.loc[df['Milemarker Number'] >= (start_loc + 52.0)]
    df = df.loc[df['Milemarker Number'] <= (end_loc + 52.0)]
    df = df.reset_index(drop = True)
    
    return df


def findYVal(direction) :
    """ Helper function that acts like a dictionary to find the Y value of an asset depedning on
    its direction.
    
    Args :
        direction : One of three possible placements on the highway : east, center, or west.
        
    Return :
        The corresponding Y coordinate value of the asset.
    """
    if(direction == 'east') :
        return 10;
    if(direction == 'center') :
        return 60;
    if(direction == 'west') :
        return 110;
        
        
def get_asset_xy_coords(df, asset_type) :
    """ From the total DataFrame, chooses one type of asset and saves its x,y coordinates into
    a list for plotting purposes.
    
    Args :
        df : Total DataFrame.
        asset_type : The type of asset that we wish to obtain the coordinate from.
        
    Return :
        2 lists : first contains the X coordinates of the assets, second contains Y coordinates.
    """
    df = df[df.Type == asset_type]
    df = df.reset_index(drop = True)
    
    xcoord, ycoord = [], []
    
    for i in range(len(df)) :
        xcoord.append(df.at[i, 'Milemarker Number'])
        ycoord.append(findYVal(df.at[i, 'Direction']))
        
    return xcoord, ycoord