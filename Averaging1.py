import h5py
from mpl_toolkits.basemap import Basemap
import threading
import numpy as np
import matplotlib.pyplot as plt
import os
import glob 

grid_size = 1 # Grid Size
grid_ctr_lons = np.arange(-180+(grid_size/2), 180+(grid_size/2), grid_size);
grid_ctr_lats = np.arange(-90+(grid_size/2), -62+(grid_size), grid_size);



year = 2021; # Year
month = 1;   # Jan
Sampling_Rate = 5;
delta = grid_size/2;
path = '/storage/scratch1/1/abrown472/Icesat2_LandIce_'+ str(year);



file_list_East_inp = glob.glob(path + '/month'+str(month)+'/East/*.h5')
file_list_West_inp = glob.glob(path + '/month'+str(month)+'/West/*.h5')

# Initialize Recursive Variables	
count = np.zeros((len(grid_ctr_lons), len(grid_ctr_lats)))
mean = np.zeros((len(grid_ctr_lons), len(grid_ctr_lats)))

def East(file_list_East):
	global mean
	global count
	for file_East in range(0, len(file_list_East)):
		
		file_path = file_list_East[file_East];	
		hf = h5py.File(file_path, 'r');
		
		alt = np.array([])
		lat = np.array([])
		lon = np.array([])
		if 'gt1l/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt1l/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt1l/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt1l/land_ice_segments/longitude')))
		if 'gt1r/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt1r/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt1r/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt1r/land_ice_segments/longitude')))
		if 'gt2l/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt2l/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt2l/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt2l/land_ice_segments/longitude')))
		if 'gt2r/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt2r/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt2r/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt2r/land_ice_segments/longitude')))
		if 'gt3l/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt3l/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt3l/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt3l/land_ice_segments/longitude')))
		if 'gt3r/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt3r/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt3r/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt3r/land_ice_segments/longitude')))
		
		alt = alt.tolist()
		lat = lat.tolist()
		lon = lon.tolist()			
		hf.close();
		ind_lon = 0;
		ind_lat = 0;
		for ind in range(0, len(alt), Sampling_Rate):
				
				
			for i in range(int(len(grid_ctr_lons)/2), len(grid_ctr_lons)):
				if (grid_ctr_lons[i]-delta < lon[ind]) and (lon[ind] < grid_ctr_lons[i]+delta):
					ind_lon = i;
					break;
			for j in range(0, len(grid_ctr_lats)):
				if (grid_ctr_lats[j]+delta > lat[ind]) and (lat[ind] > grid_ctr_lats[j]-delta):
					ind_lat = j;
					break;										
			if alt[ind] < 6000000000:
				count[ind_lon, ind_lat] = count[ind_lon, ind_lat] + 1;
				mean[ind_lon, ind_lat] = mean[ind_lon, ind_lat] + ((alt[ind] - mean[ind_lon, ind_lat])/count[ind_lon, ind_lat])
				#print('East' +' '+ str(ind) +' '+ str(len(alt))+ ' '+ str(mean[ind_lon, ind_lat]))

def West(file_list_West):
	global mean
	global count
	for file_West in range(0, len(file_list_West)): 		
		
		file_path = file_list_West[file_West];	
		hf = h5py.File(file_path, 'r');
		alt = np.array([])
		lat = np.array([])
		lon = np.array([])
		if 'gt1l/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt1l/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt1l/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt1l/land_ice_segments/longitude')))
		if 'gt1r/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt1r/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt1r/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt1r/land_ice_segments/longitude')))
		if 'gt2l/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt2l/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt2l/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt2l/land_ice_segments/longitude')))
		if 'gt2r/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt2r/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt2r/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt2r/land_ice_segments/longitude')))
		if 'gt3l/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt3l/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt3l/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt3l/land_ice_segments/longitude')))

		if 'gt3r/land_ice_segments/h_li' in hf.keys():			 
			alt = np.append(alt, np.array(hf.get('gt3r/land_ice_segments/h_li')))
			lat = np.append(lat, np.array(hf.get('gt3r/land_ice_segments/latitude')))
			lon = np.append(lon, np.array(hf.get('gt3r/land_ice_segments/longitude')))

		alt = alt.tolist()
		lat = lat.tolist()
		lon = lon.tolist()			
		hf.close();
			
		ind_lon = 0;
		ind_lat = 0;
		for ind in range(0, len(alt), Sampling_Rate):
			for i in range(0, int(len(grid_ctr_lons)/2)-1):
				if (grid_ctr_lons[i]-delta < lon[ind]) and (lon[ind] < grid_ctr_lons[i]+delta):
					ind_lon = i;
					break;
			for j in range(0, len(grid_ctr_lats)):
				if (grid_ctr_lats[j]+delta > lat[ind]) and (lat[ind] > grid_ctr_lats[j]-delta):
					ind_lat = j;
					break;										
			if alt[ind] < 6000000000:
				count[ind_lon, ind_lat] = count[ind_lon, ind_lat] + 1;
				mean[ind_lon, ind_lat] = mean[ind_lon, ind_lat] + ((alt[ind] - mean[ind_lon, ind_lat])/count[ind_lon, ind_lat])
				#print('West' +' '+ str(ind) +' '+ str(len(alt))+ ' '+ str(mean[ind_lon, ind_lat]))
							
p1 = threading.Thread(target = East, args=(file_list_East_inp,))
p2 = threading.Thread(target = West, args=(file_list_West_inp,))
p1.start()
p2.start()
p1.join()
p2.join()
	
	
print('Month Complete Writing to file')
with open(path+'/Averaged'+str(month)+'_'+str(year)+'.txt', 'w') as file:
	for i in range(0, len(grid_ctr_lons)):
		for j in range(0, len(grid_ctr_lats)):
			string = str(grid_ctr_lons[i]) + ',' + str(grid_ctr_lats[j]) + ',' + str(mean[i,j]) + '\n';
			file.write(string);
			 
print("Complete Writing to file")

	
	

