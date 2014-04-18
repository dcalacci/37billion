import pandas as pd
import utils
import shapely.geometry
import shapely
import fiona
import os


def create_nearest_distance_df():
    # dataframe with trains info
    trains_df = pd.read_csv('../notebooks/trains_df.p')

    # has grid location info
    grid_loc_df = pd.read_csv('../notebooks/grid_loc_df.csv')

    closest_dist = []
    nearest_station = []

    for n, row in grid_loc_df.iterrows():
        if n % 1000 == 0:
            print "processed ", float(n)/len(grid_loc_df)*100, "% of elements."
        res = utils.get_nearest_station((float(row.x), float(row.y)), trains_df)

        nearest_station.append(res[0])
        closest_dist.append(res[1])

    grid_loc_df['closest_distance'] = closest_dist
    grid_loc_df['nearest_station'] = nearest_station
    grid_loc_df.to_pickle('grid_loc_df_with_dist.p')


def create_shapefile(shapefile, grid_df):
    with fiona.open(shapefile, 'r') as grids:

        schema = grids.schema.copy()
        properties = schema['properties'].items()
        properties.append(('closest_distance', 'float'))
        properties.append(('nearest_station', 'int'))
        schema['properties'] = dict(properties)

        with fiona.collection('join_data_grids.shp', 'w', 'ESRI Shapefile',
                              schema=schema,
                              crs=shapefile.crs,
                              driver=shapefile.driver) as output:
            count = 0
            for shapefile_record in grids:
                count += 1
                if count % 1000 == 0:
                    p = float(count)/len(grids)*100
                    print "processed", p, "% of records"

                gid = shapefile_record['properties']['g250m_id']
                nearest_station = grid_df.ix[gid]['nearest_station']
                closest_distance = grid_df.ix[gid]['closest_distance']

                shapefile_record['properties']['closest_distance'] = closest_distance
                shapefile_record['properties']['nearest_station'] = nearest_station
                output.write(shapefile_record)
