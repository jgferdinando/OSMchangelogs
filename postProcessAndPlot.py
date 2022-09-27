# intended for Google Colab

# start block 1

import json
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from google.colab import drive
try:
  import geopandas as gpd
  from geopandas import GeoDataFrame
except:
  !pip install geopandas
  import geopandas as gpd
  from geopandas import GeoDataFrame
  
  # end block 1
  
  # start block 2
  
  #drive.mount('/content/gdrive/', force_remount=True)

df = pd.read_csv('osm_0004.csv')
#make datetime column that can be sorted
df['closed_at'] =  pd.to_datetime(df['closed_at'], format="%Y-%m-%dT%H:%M:%SZ")
print(df.head(5))
oldest = df['closed_at'].min()
newest = df['closed_at'].max()
print(oldest)
print(newest)
#filter large edit areas
df = df.dropna(subset=['min_lat','min_lon','max_lat','max_lon'])
df['extent_lat'] = abs(df['max_lat'] - df['min_lat'])
df['extent_lon'] = abs(df['max_lon'] - df['min_lon'])
maxLatExtent = 10
maxLonExtent = 10
df = df[df['extent_lat'] <= maxLatExtent]
df = df[df['extent_lon'] <= maxLonExtent]
#print(len(df))
#find centroids and plot
df['cent_lat'] = (df['max_lat'] + df['min_lat']) / 2
df['cent_lon'] = (df['max_lon'] + df['min_lon']) / 2
geometry = [Point(xy) for xy in zip(df['cent_lon'], df['cent_lat'])]
gdf = GeoDataFrame(df, geometry=geometry,crs=4326) 
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
gdf.plot(ax=world.plot(figsize=(30, 15), color='whitesmoke'), marker='+', color='black', markersize=50);
df.to_csv('osm_0004_postprocessed.csv')

# end block 2

# start block 3

citydf = pd.read_csv('cities1000.txt', sep='\t')
print(citydf)

# end block 3

# start block 4

citydf['latround'] = citydf['latitude'].round(decimals=1)
citydf['lonround'] = citydf['longitude'].round(decimals=1)
groupedCityDF = citydf.groupby(['latround','lonround']).sum()
print(groupedCityDF)
df['latround'] = df['cent_lat'].round(decimals=1)
df['lonround'] = df['cent_lon'].round(decimals=1)
groupedChangeDF = df.groupby(['latround','lonround']).sum()
print(groupedChangeDF)
mergedDF = groupedChangeDF.merge(groupedCityDF, how='inner', on=['latround','lonround'])
print(mergedDF)

# end block 4

# start block 5

fig = plt.figure(figsize=(8,8), dpi=150, constrained_layout=True)
ax1 = fig.add_subplot(111)
ax1.scatter(mergedDF['population'], mergedDF['num_changes'],marker="+",s=2)
ax1.set_ylim([0, 500000])
ax1.set_xlim([0, 500000])
#ax1.set_xscale('log')
#ax1.set_yscale('log')
ax1.set_xlabel('Population')
ax1.set_ylabel('Number of Changes')

#end block 5
