#import requires packages
import fiona
import pandas as pd
import rasterio
import numpy as np

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

def get_vent_shp(run_outs, path_to_folder, flow_id):
    # import points from slope file
    pointDf = pd.read_csv(run_outs, header=0, sep=',')
    pointDf.head()
    # define schema for line shape file
    schema = {'geometry': 'Point', 'properties': [("flow_id", 'str'),]}
    # open a fiona object
    name_vent = 'vent_' + flow_id + '.shp'
    pointShp = fiona.open(path_to_folder+'map/' + name_vent, mode='w',
                         driver='ESRI Shapefile', schema=schema, crs="EPSG:32740")

    # iterate over each row in the dataframe and save record
    for index, row in pointDf.iterrows():
        rowDict = {
            'geometry': {'type': 'Point',
                         'coordinates': (row.X_init, row.Y_init)},
            'properties': {'flow_id': row.flow_id,
                           }}
        pointShp.write(rowDict)
    # close fiona object
    pointShp.close()

def crop_asc_file(sim_asc, path_to_folder, flow_id):
    cropped_asc_file = path_to_folder + '/map/sim_' + flow_id + '.asc'
    with open(sim_asc) as file:
        header_lines = [next(file) for _ in range(6)]
        ncols = int(header_lines[0].split()[1])
        nrows = int(header_lines[1].split()[1])
        xllcorner = float(header_lines[2].split()[1])
        yllcorner = float(header_lines[3].split()[1])
        cellsize = float(header_lines[4].split()[1])
        nodata_value = float(header_lines[5].split()[1])
        # Read the values from the ASC file
        data_lines = [line.strip().split() for line in file]
        # Convert the data lines to a NumPy array
        data = np.array(data_lines, dtype=float)
    # Determine the index of the non-zeros lines and columns
    nonzero_rows, nonzero_cols = np.nonzero(data)
    # Calculate the limit of the crop
    min_row, max_row = np.min(nonzero_rows), np.max(nonzero_rows)
    min_col, max_col = np.min(nonzero_cols), np.max(nonzero_cols)
    # Defnie the values of the cropped data
    cropped_data = data[min_row:max_row + 1, min_col:max_col + 1]
    # Update the headers of the new cropped asc file
    cropped_nrows, cropped_ncols = cropped_data.shape
    cropped_xllcorner = xllcorner + min_col * cellsize
    cropped_yllcorner = yllcorner + (nrows - max_row - 1) * cellsize
    header_lines = [
        f"ncols {cropped_ncols}\n",
        f"nrows {cropped_nrows}\n",
        f"xllcorner {cropped_xllcorner}\n",
        f"yllcorner {cropped_yllcorner}\n",
        f"cellsize {cellsize}\n",
        f"nodata_value {nodata_value}\n"
    ]
    # write data in the new cropped asc file
    with open(cropped_asc_file, "w") as file:
        file.writelines(header_lines)
        for row in cropped_data:
            line = " ".join(str(value) if value is not None else str(nodata_value) for value in row)
            file.write(line + "\n")

def convert_to_tiff(cropped_asc_file, path_to_folder, flow_id):
    # Convert the .asc file to a compressed GeoTIFF (.tif)
    sim_tif_file = path_to_folder + 'map/'+'sim_' + flow_id + '.tif'
    with rasterio.open(cropped_asc_file) as src:
        profile = src.profile.copy()
        profile["compress"] = "deflate"  # Use deflate compression
        profile["tiled"] = True  # Enable tiling for better performance and compression
        profile["blockxsize"] = 128  # Adjust the tile size as needed
        profile["blockysize"] = 128
        data = src.read(1)
        with rasterio.open(sim_tif_file, "w", **profile) as dst:
            dst.write(data, 1)
