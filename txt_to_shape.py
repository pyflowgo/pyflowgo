#import requires packages
import fiona
import pandas as pd

def get_path_shp(slope_file, path_to_folder,flow_id):
    # import points from slope file
    lineDf = pd.read_csv(slope_file, header=0, sep='\t')
    lineDf.head()
    # define schema for line shape file
    schema = {'geometry': 'LineString', 'properties': [('L', 'str')]}
    # open a fiona object
    name = 'path_'+flow_id+'.shp'
    lineShp = fiona.open(path_to_folder+'map/' + name, mode='w',
                         driver='ESRI Shapefile', schema=schema, crs="EPSG:32740")

    # get list of points
    xyList = []
    rowName = ''
    for index, row in lineDf.iterrows():
        xyList.append((row.x, row.y))
        rowName = row.L

    # save record and close shapefile
    rowDict = {'geometry': {'type': 'LineString', 'coordinates': xyList}, 'properties': {'L': rowName}, }
    lineShp.write(rowDict)
    # close fiona object
    lineShp.close()

def get_runouts_shp(run_outs, path_to_folder, flow_id):
    # import points from slope file
    pointDf = pd.read_csv(run_outs, header=0, sep=',')
    pointDf.head()
    # define schema for line shape file
    schema = {'geometry': 'Point', 'properties': [("flow_id", 'str'), ("Effusion_rate", 'int'),
                                                  ("Depth", 'float'),("Width_init", 'float'),
                                                  ("Elevation_run_out", 'int'),("Distance_run_out", 'int')
                                                   ]}
    # open a fiona object
    name_runouts = 'run_outs_' + flow_id + '.shp'
    pointShp = fiona.open(path_to_folder+'map/' + name_runouts, mode='w',
                         driver='ESRI Shapefile', schema=schema, crs="EPSG:32740")

    # iterate over each row in the dataframe and save record
    for index, row in pointDf.iterrows():
        rowDict = {
            'geometry': {'type': 'Point',
                         'coordinates': (row.X_run_out, row.Y_run_out)},
            'properties': {'flow_id': row.flow_id, 'Effusion_rate': row.Effusion_rate,
                           'Depth': row.Depth, 'Width_init': row.Width_init,
                           'Elevation_run_out': row.Elevation_run_out, 'Distance_run_out': row.Distance_run_out,
                           }}
        pointShp.write(rowDict)
    # close fiona object
    pointShp.close()
