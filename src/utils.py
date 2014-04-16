#!/usr/bin/env python
import shapely, fiona, sys
import pandas as pd


def get_nearest_station(coords, df):
    df = df[df['amtrak'] == False]
    df = df[df['commuter'] == True]
    # print coords
    df['dist']= df['coordinates'].apply(lambda pt: shapely.geometry.Point(pt[0], pt[1]).distance(shapely.geometry.Point(coords[0], coords[1])))
    # print set(list(df['dist']))
    mindist = df['dist'].idxmin()
    return (mindist, df.ix[mindist]['dist'])


def logged_apply(g, func, *args, **kwargs):
    step_percentage = 100. / len(g)
    import sys
    sys.stdout.write('apply progress:   0%')
    sys.stdout.flush()

    def logging_decorator(func):
        def wrapper(*args, **kwargs):
            progress = wrapper.count * step_percentage
            sys.stdout.write('\033[D \033[D' * 4 + format(progress, '3.0f') + '%')
            sys.stdout.flush()
            wrapper.count += 1
            return func(*args, **kwargs)
        wrapper.count = 0
        return wrapper

    logged_func = logging_decorator(func)
    res = g.apply(logged_func)
    sys.stdout.write('\033[D \033[D' * 4 + format(100., '3.0f') + '%' + '\n')
    sys.stdout.flush()
    return res
