import pandas as pd
import utils
import shapely.geometry
import shapely
import fiona
import os

# dataframe with trains info
trains_df = pd.read_csv('../notebooks/trains_df.p')

# has grid location info
grid_loc_df = pd.read_csv('../notebooks/grid_loc_df.csv')


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


def create_shapefile(shapefile, grid_df):
    with fiona.open(shapefile, 'r') as grids:

        schema = grids.schema.copy()
        schema['properties']['nearest_station'] = 'int'
        schema['properties']['nearest_dist'] = 'float'

        with fiona.collection('join-data_grids.shp', 'w', 'ESRI Shapefile', schema) as output:
            for shapefile_record in grids:
                gid = shapefile_record['properties']['g250m_id']
                closest_station = grid_df[gid]['closest_station']
                nearest_distance = grid_df[gid]['nearest_distance']
                shapefile_record['properties']['nearest_distance'] = nearest_distance
                shapefile_record['properties']['closest_station'] = closest_station
                output.write(shapefile_record)
