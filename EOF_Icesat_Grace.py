import numpy as np
import glob
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
import scipy.linalg as LA
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
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
Grace_data = np.zeros((36, length));   # Equivalent Sea-Water Thickness from 180x180 Gravity data

path = '/storage/scratch1/1/abrown472'

# Load GRACE Data
monthnum = 0;
for year in range(19, 21 +1):
    for month in range(1, 12 + 1):
        if year == 2019:
            monthnum = 0
        elif year == 2020:
            monthnum = 12
        elif year == 2021:
            monthnum = 24
        if month >=1 and month <=9:
            mon = str(0) + str(month);
        elif month >= 10 and month <=12:
            mon = str(month);
        
        file_path = path+'/GRACE/'+str(year)+'_'+mon+'.txt'
        #print(file_path)
        with open(file_path) as file:
            for index in range(0, length):
                line = file.readline()
                line = line.split(',');	
                lons[0, index] = float(line[0])
                lats[0, index] = float(line[1])
                Grace_data[monthnum + month -1, index] = float(line[2])
                			
# Load Icesat Data
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

# Remove NaN columns
index = [];
flag = 0;
for i in range(0, cols):
    for j in range(0, rows):
        if Grace_data[j, i] == -999999.000:
            Grace_data[j,i] = 0;
            flag = 1;
            break;
    if flag == 0:
        index.extend([i])
    elif flag == 1:
        flag = 0;

              
data1 = Icesat2_data[:, index[:]]
data2 = Grace_data[:, index[:]]
lons_new = lons[0, index[:]]
lats_new = lats[0, index[:]]
N = 36
M = 7681



# Detrending Data
for i in range(0, M):
    avg = np.mean(data1[:, i]);
    data1[:,i] = data1[:,i] - avg;
    
    avg = np.mean(data2[:, i]);
    data2[:,i] = data2[:,i] - avg;
    

cov = (data1.transpose()@data2)/N; 

U, S, VT = np.linalg.svd(cov)

EOF = VT.transpose();

# Modes
L = np.power(S,2)/np.sum(np.power(S,2))*100;
Mode1 = L[0];
Mode2 = L[1];
Mode3 = L[3];
print(S)
print(Mode1)
print(Mode2)
print(Mode3)

# Expansion Coefficients

Icesat = data1@U
Grace = data2@VT.transpose()

'''
with open('TemporalModes_IG.txt', 'w') as file:
    for i in range(0, N):
        file.write(str(round(Icesat[i,0],6))+','+str(round(Icesat[i,1],6))+','+str(round(Icesat[i,2],6))
        +','+ str(round(Grace[i,0],6))+','+str(round(Grace[i,1],6))+','+str(round(Grace[i,2],6))+'\n')

t = np.arange(1,36+1,1)

fig = plt.figure()
axis1 = fig.add_subplot(211)
axis1.plot(t, Icesat[:, 1])

axis2 = fig.add_subplot(212)
axis2.plot(t, Grace[:, 1])
fig.savefig('Icesat_Grace_Mode2.png')
'''

S[3:-1] = 0;
Recon_data = U@np.diag(S)@VT;


# Plotting Results    
lons = np.arange(-180+(grid_size/2), 180+(grid_size/2), grid_size);
lats = lats[0, 0:28];

lon, lat = np.meshgrid(lons, lats)
interpZ = griddata((lons_new[:], lats_new[:]), Recon_data[12, :], (lon, lat), method='linear')
alt = np.zeros((len(lats), len(lons)));

'''
i = 0; j = 0;

for k in range(0, length):
    alt[i,j] = grid_z0[k];
    #print(alt[i,j])
    i = i + 1;
    if i == len(lats):
        i = 0;
        j = j + 1;
    if j == len(lons):
        j = 0;
'''
m = Basemap(projection='spstere',boundinglat=-63,lon_0=-180,resolution='l')
x,y = m(lon, lat)
#levels = np.linspace(-20, 400,50);
#m.scatter(x,y, c= alt, s =0.7, cmap = 'tab20b', norm = matplotlib.colors.LogNorm())
#m.fillcontinents(color='coral',lake_color='aqua')
m.contourf(x,y,interpZ,cmap='PuBu');

# draw parallels and meridians.
m.drawcoastlines()
m.drawparallels(np.arange(-90,-63, 4), labels = [1,1,1,1])
m.drawmeridians(np.arange(-180,180,20), labels = [1,1,1,1])
#m.drawmapboundary(fill_color='aqua')
plt.colorbar(orientation = 'horizontal')

plt.show()
plt.savefig('Icesat_Grace_Cov12.png')
