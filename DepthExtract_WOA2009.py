# quick script to slice WOA 2009 NetCDF files by depth and convert to individual GeoTIFFs
# WOA data from: http://www.nodc.noaa.gov/OC5/WOA09/netcdf_data.html

# need to examine each NC file first to get:
	## depth bin band numbers (add to Depth_Bins array below)
		### look at NETCDF_DIM_depth=nnnn for each Band number
	
	## use GDALINFO like -> gdalinfo NETCDF:"apparent_oxygen_utilization_annual_1deg.nc":A_an

# requires GDAL 1.10.0 or later

import os

WOA_Dir = '/Users/jcleary/Desktop/DSP_data/WOA'
Output_Dir = '/Users/jcleary/Desktop/DSP_data/WOA'

# Band numbers are the same across all WOA NC files
Depth_Bands = {1:'surface', 7:'100m', 10:'200m', 14:'500m', 15:'600m', 19:'1000m', 28:'3000m', 32:'5000m'}  

# no scale_factor or add_offset for these files
# see http://www.nodc.noaa.gov/OC5/WOA09/netcdf_data.html for NC metadata
Variables ={'apparent_oxygen_utilization':{'NCfile':WOA_Dir+'/apparent_oxygen_utilization/apparent_oxygen_utilization_annual_1deg.nc','SD_Name':'A_an'},
			'dissolved_oxygen':{'NCfile':WOA_Dir+'/dissolved_oxygen/dissolved_oxygen_annual_1deg.nc','SD_Name':'o_an'},
			'nitrate':{'NCfile':WOA_Dir+'/nitrate/nitrate_annual_1deg.nc','SD_Name':'n_an'},
			'oxygen_saturation':{'NCfile':WOA_Dir+'/oxygen_saturation/oxygen_saturation_annual_1deg.nc','SD_Name':'O_an'},
			'phosphate':{'NCfile':WOA_Dir+'/phosphate/phosphate_annual_1deg.nc','SD_Name':'p_an'},
			'salinity':{'NCfile':WOA_Dir+'/salinity/salinity_annual_1deg.nc','SD_Name':'s_an'},
			'silicate':{'NCfile':WOA_Dir+'/silicate/silicate_annual_1deg.nc','SD_Name':'i_an'},
			'temperature':{'NCfile':WOA_Dir+'/temperature/temperature_annual_1deg.nc','SD_Name':'t_an'},
			}

for Var,Var_Specs in Variables.iteritems():
	print
	print Var
	print Var_Specs
	
	for Band,Depth in Depth_Bands.iteritems():
		print 'Band:' +str(Band)+ ' ' + Depth
		Output_File = '%s/%s/WOA2009_%s__%s.tif' % (Output_Dir,Var,Var,Depth)
		
		GDAL_Convert = 'gdal_translate -of GTiff -a_srs EPSG:4326 -b %s NETCDF:"%s":%s %s' % (Band,Var_Specs['NCfile'],Var_Specs['SD_Name'],Output_File)
		os.system(GDAL_Convert) 
		
	print Var + " completed"
	print