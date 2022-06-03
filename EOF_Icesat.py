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

# Detrending Data
for i in range(0, cols):
    avg = np.mean(Icesat2_data[:, i]);
    Icesat2_data[:,i] = Icesat2_data[:,i] - Icesat2_data[0,i];
    #Icesat2_data[:,i] = Icesat2_data[:,i]- avg;
   

# SVD
data = Icesat2_data;
U, S, VT = np.linalg.svd(data)
#np.set_printoptions(threshold=np.inf)
EOF = VT.transpose();

# Modes
L = np.power(S,2)/np.sum(np.power(S,2))*100;
Mode1 = L[0];
Mode2 = L[1];
Mode3 = L[3];
print(Mode1)
print(Mode2)
print(Mode3)
EC = np.dot(U, np.diag(S))

t = np.arange(1,36+1,1)
plt.plot(t, EC[:, 2])
plt.show()
plt.savefig('oscil.png')

with open('TemporalModes_IcesatOnly.txt', 'w') as file:
    for i in range(0, 36):
        file.write(str(round(EC[i,0],6))+','+str(round(EC[i,1],6))+','+str(round(EC[i,2],6))+'\n')

S[2:-1] = 0;
S[0] = 0;
Recon_data = U@LA.diagsvd(S, *data.shape)@VT;


# Plotting Results    
lons = np.arange(-180+(grid_size/2), 180+(grid_size/2), grid_size);
lats = lats[0, 0:28];
lon, lat = np.meshgrid(lons, lats)
alt = np.zeros((len(lats), len(lons)));
i = 0; j = 0;
for k in range(0, length):
    alt[i,j] = Recon_data[1, k];
    i = i + 1;
    if i == len(lats):
        i = 0;
        j = j + 1;
    if j == len(lons):
        j = 0;

m = Basemap(projection='spstere',boundinglat=-63,lon_0=-180,resolution='l')
x,y = m(lon, lat)
levels = np.linspace(-50, 300, 400);
#m.scatter(x,y, c= alt, s =0.7, cmap = 'tab20b', norm = matplotlib.colors.LogNorm())
#m.fillcontinents(color='coral',lake_color='aqua')
m.contourf(x,y,alt,cmap='PuBu', levels = levels);

# draw parallels and meridians.
m.drawcoastlines()
m.drawparallels(np.arange(-90,-63, 4), labels = [1,1,1,1])
m.drawmeridians(np.arange(-180,180,20), labels = [1,1,1,1])
#m.drawmapboundary(fill_color='aqua')
plt.colorbar(orientation = 'horizontal')

plt.show()
plt.savefig('EOF_Icesat_Mode2.png')
