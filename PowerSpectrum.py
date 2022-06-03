import numpy as np
import glob
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
import scipy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib
grid_size = 1
grid_ctr_lons = np.arange(-180+(grid_size/2), 180+(grid_size/2), grid_size);
grid_ctr_lats = np.arange(-90+(grid_size/2), -62+(grid_size), grid_size);

length = (len(grid_ctr_lats)-1) * len(grid_ctr_lons)
lats = np.zeros((1, length))
lons = np.zeros((1, length))
Max_Eig = np.zeros((1, length))

# Data Placeholders
Icesat2_data = np.zeros((36, length)); # Averaged Land-Ice Level-3 data

path = '/storage/scratch1/1/abrown472'

# Load Icesat Data

length = (len(grid_ctr_lats)-1) * len(grid_ctr_lons)
monthnum = 0;
for year in range(2019, 2021 +1):
    for month in range(1, 12 +1):
        if year == 2019:
            monthnum = 0
        elif year == 2020:
            monthnum = 12
        elif year == 2021:
            monthnum = 24
        file_path = path+ '/Averaged'+str(year)+'_1grid'+'/Averaged'+str(month)+'_'+str(year)+'.txt'
        #print("Main: "+ str(monthnum + month -1))
        with open(file_path) as file:
            i = 0
            for index in range(0, length):
                line = file.readline()
                line = line.split(',');
                if float(line[1]) != -61.5:
                    lons[0, i] = float(line[0]);
                    lats[0, i] = float(line[1]);
                    Icesat2_data[monthnum + month -1, i] = float(line[2])
                    i= i+1;
                
				#print(index)				

rows = Icesat2_data.shape[0]
cols = Icesat2_data.shape[1]			
index = 0;
print(lons)
for i in range(0, length):
	if lons[0, i] == -104.5 and lats[0, i] == -77.5:
		index = i;
		print('Found')
		break;

with open('Loc_neg104.5_neg77.5.txt', 'w') as file:
	for i in range(0, rows):
		file.write(str(round(Icesat2_data[i, index],6))+'\n')
	

