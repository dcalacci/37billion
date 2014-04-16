import pandas as pd
import utils
import shapely.geometry
import shapely
import fiona
import os

# dataframe with trains info
trains_df = pd.read_csv('../data/trans_df.csv')

# has grid location info
grid_loc_df = pd.read_csv('../data/grid_loc.csv')


def create_nearest_distance_df():
    closest_dist = []
    nearest_station = []

    for n, row in grid_loc_df.iterrows():
        if n % 10000 == 0:
            print "processed ", float(n)/len(grid_loc_df)*100, "% of elements."
        res = utils.get_nearest_station((row.x, row.y), trains_df)

        nearest_station.append(res[0])
        closest_dist.append(res[1])

    grid_loc_df['closest_distance'] = closest_dist
    grid_loc_df['nearest_station'] = nearest_station
    grid_loc_df.to_csv('grid_loc_df_with_dist.csv')
