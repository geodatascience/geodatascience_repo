+++
author = "François Pacull"
categories = ["Python", "GeoPandas", "Shapefile"]
date = "2019-07-31"
description = ""
featured = ""
featuredalt = ""
featuredpath = "date"
linktitle = ""
title = "An Introduction to GeoPandas"
type = "post"

+++

We are going to explore some geospatial data from the european Urban Atlas with the Python package [**GeoPandas**]((https://geopandas.readthedocs.io/en/latest/)). Here is a short description of these data from [this](https://www.eea.europa.eu/data-and-maps/data/copernicus-land-monitoring-service-urban-atlas) website:
 
> The European Urban Atlas provides reliable, inter-comparable, high-resolution land use maps for over [...] 800 Functional Urban Area (FUA) and their surroundings (more than 50.000 inhabitants) for the 2012 reference year in EEA39.

Data for the city of Lyon, France, is downloaded from the [Urban Atlas 2012](https://land.copernicus.eu/local/urban-atlas/urban-atlas-2012/view) page and then uncompressed in a local `data/` directory.
From the compressed archive, we got 3 [shapefiles](https://en.wikipedia.org/wiki/Shapefile) in the shapefile folder:
- FR003L2_LYON_CityBoundary
- FR003L2_LYON_UA2012
- FR003L2_LYON_UA2012_Boundary

This post is mainly inspired from [this](https://github.com/jorisvandenbossche/geopandas-demo/blob/master/geopandas_demo.ipynb) notebook by [Joris Van den Bossche](https://twitter.com/jorisvdbossche?lang=fr), the main developper of [geopandas](https://geopandas.readthedocs.io/en/latest/). 

Let's start by describing how we created the environment, and import the packages.

## Environment & package installation

We installed the following packages with anaconda:
```bash
conda create -n urban_atlas python=3.7
conda activate urban_atlas
conda install -y pandas jupyterlab matplotlib
conda install -y descartes mapclassify
conda install -y geopandas colorcet
pip install contextily
```
Here are the main packages' version:

| Package    | Version |
|---|---|
| geopandas  | 0.5.1 |
| pandas     | 0.25.0 |
| matplotlib | 3.1.1 |
| numpy      | 1.16.4 |
| colorcet   | 1.0.0 |
| contextily | 0.99.0.dev |
    
After importing the packages, we are now ready to load the shapefiles.

## Data loading

Shapefiles are loaded into geodataframes:


```python
%%time
lyon_CityBoundary = gpd.read_file(FR003L2_LYON_CityBoundary_path)
lyon_UA2012 = gpd.read_file(FR003L2_LYON_UA2012_path)
lyon_UA2012_Boundary = gpd.read_file(FR003L2_LYON_UA2012_Boundary_path)
```

    CPU times: user 5.69 s, sys: 270 ms, total: 5.96 s
    Wall time: 5.91 s


The two boundary shapefiles only have one row, each one with the respective boundary geometries (city and urban area). They also have some geographic attributes about the areas. The `lyon_UA2012` geodataframe is more massive:


```python
lyon_UA2012.shape
```
    (94614, 11)

It seems that there is no missing value:

```python
lyon_UA2012.isna().any().any()
```
    False
Here are the dataframe's columns:

```python
lyon_UA2012.columns
```

    Index(['COUNTRY', 'CITIES', 'FUA_OR_CIT', 'CODE2012', 'ITEM2012', 'PROD_DATE',
           'IDENT', 'Shape_Leng', 'Shape_Area', 'Pop2012', 'geometry'],
          dtype='object')

Later we will describe these attributes. Let's start by plotting the city and urban area boundaries, with background tiles. 

## Plot a map with background tiles

The [contextily](https://github.com/darribas/contextily) package is used to add the tiles (see geopandas' documentation [here](http://geopandas.org/gallery/plotting_basemap_background.html)). We also need to convert the geodataframe geometries to Web Mercator (EPSG 3857) at the same time, in order to match the projection of the tiles:


```python
lyon_CityBoundary = lyon_CityBoundary.to_crs(epsg=3857)
lyon_UA2012 = lyon_UA2012.to_crs(epsg=3857)
lyon_UA2012_Boundary = lyon_UA2012_Boundary.to_crs(epsg=3857)
```

Now we can plot the two boundary shapefiles:

```python
# this function is taken from http://geopandas.org/gallery/plotting_basemap_background.html
def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    # tiles: terrain, terrain-background, terrain-labels, terrain-lines, toner, 
    # toner-background, toner-hybrid, toner-lines, toner-lite, watercolor
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    ax.axis((xmin, xmax, ymin, ymax)) # restore original x/y limits
```


```python
ax = lyon_UA2012_Boundary.plot(figsize=figsize_S, color='g', alpha=0.5);
lyon_CityBoundary.plot(ax=ax, color='y', alpha=0.5);
add_basemap(ax, zoom=10);
plt.axis('off');
```

![png](../../img/2019/07/output_14_0.jpg)

We can see on this map the urban area and the metropolitan region of Lyon (the inner boundary).

Now let's look at the attributes the larger shapefile.

## Land use and land cover data

### Zonal attributes


```python
lyon_UA2012.head(2)
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>COUNTRY</th>
      <th>CITIES</th>
      <th>FUA_OR_CIT</th>
      <th>CODE2012</th>
      <th>ITEM2012</th>
      <th>PROD_DATE</th>
      <th>IDENT</th>
      <th>Shape_Leng</th>
      <th>Shape_Area</th>
      <th>Pop2012</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>FR</td>
      <td>Lyon</td>
      <td>FR003L2</td>
      <td>11100</td>
      <td>Continuous urban fabric (S.L. : &gt; 80%)</td>
      <td>2015</td>
      <td>1-FR003L2</td>
      <td>269.157363</td>
      <td>3336.206536</td>
      <td>13</td>
      <td>POLYGON ((557163.6322599069 5691021.665466284,...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>FR</td>
      <td>Lyon</td>
      <td>FR003L2</td>
      <td>11100</td>
      <td>Continuous urban fabric (S.L. : &gt; 80%)</td>
      <td>2015</td>
      <td>2-FR003L2</td>
      <td>298.965906</td>
      <td>1536.998514</td>
      <td>7</td>
      <td>POLYGON ((530679.8832735929 5692765.775455, 53...</td>
    </tr>
  </tbody>
</table>
</div>



For each geometry, we have the following attributes:
- `COUNTRY`: country code, always `FR`
- `CITIES`: main city, always `Lyon`
- `FUA_OR_CIT`: urban area code, always `FR003L2`
- `CODE2012`: code for the geographic type of the area covered by the geometry
- `ITEM2012`: label of the geographic type of the area covered by the geometry
- `PROD_DATE`: production date, always `2015`
- `IDENT`: unique area identifier
- `Shape_Leng`: maximum length of the geometry (m)
- `Shape_Area`: area of the geometry (m2)
- `Pop2012`: population living in the area covered by the geometry

### Geographic types

Here are the different geographic types found in the table:


```python
codes = lyon_UA2012[['CODE2012', 'ITEM2012']].drop_duplicates().reset_index(drop=True)
pd.set_option('display.max_colwidth', -1)
codes
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CODE2012</th>
      <th>ITEM2012</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>11100</td>
      <td>Continuous urban fabric (S.L. : &gt; 80%)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>11210</td>
      <td>Discontinuous dense urban fabric (S.L. : 50% -  80%)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>11220</td>
      <td>Discontinuous medium density urban fabric (S.L. : 30% - 50%)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>11230</td>
      <td>Discontinuous low density urban fabric (S.L. : 10% - 30%)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>11240</td>
      <td>Discontinuous very low density urban fabric (S.L. : &lt; 10%)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>11300</td>
      <td>Isolated structures</td>
    </tr>
    <tr>
      <th>6</th>
      <td>12100</td>
      <td>Industrial, commercial, public, military and private units</td>
    </tr>
    <tr>
      <th>7</th>
      <td>12300</td>
      <td>Port areas</td>
    </tr>
    <tr>
      <th>8</th>
      <td>12400</td>
      <td>Airports</td>
    </tr>
    <tr>
      <th>9</th>
      <td>13100</td>
      <td>Mineral extraction and dump sites</td>
    </tr>
    <tr>
      <th>10</th>
      <td>13300</td>
      <td>Construction sites</td>
    </tr>
    <tr>
      <th>11</th>
      <td>13400</td>
      <td>Land without current use</td>
    </tr>
    <tr>
      <th>12</th>
      <td>14100</td>
      <td>Green urban areas</td>
    </tr>
    <tr>
      <th>13</th>
      <td>14200</td>
      <td>Sports and leisure facilities</td>
    </tr>
    <tr>
      <th>14</th>
      <td>21000</td>
      <td>Arable land (annual crops)</td>
    </tr>
    <tr>
      <th>15</th>
      <td>22000</td>
      <td>Permanent crops (vineyards, fruit trees, olive groves)</td>
    </tr>
    <tr>
      <th>16</th>
      <td>23000</td>
      <td>Pastures</td>
    </tr>
    <tr>
      <th>17</th>
      <td>31000</td>
      <td>Forests</td>
    </tr>
    <tr>
      <th>18</th>
      <td>32000</td>
      <td>Herbaceous vegetation associations (natural grassland, moors…)</td>
    </tr>
    <tr>
      <th>19</th>
      <td>33000</td>
      <td>Open spaces with little or no vegetation (beaches, dunes, bare rocks, glaciers)</td>
    </tr>
    <tr>
      <th>20</th>
      <td>40000</td>
      <td>Wetlands</td>
    </tr>
    <tr>
      <th>21</th>
      <td>50000</td>
      <td>Water</td>
    </tr>
    <tr>
      <th>22</th>
      <td>12220</td>
      <td>Other roads and associated land</td>
    </tr>
    <tr>
      <th>23</th>
      <td>12230</td>
      <td>Railways and associated land</td>
    </tr>
    <tr>
      <th>24</th>
      <td>12210</td>
      <td>Fast transit roads and associated land</td>
    </tr>
  </tbody>
</table>
</div>



Actually we can set these two columns as categorical in the larger dataframe, instead of string:


```python
lyon_UA2012[['CODE2012', 'ITEM2012']].dtypes
```




    CODE2012    object
    ITEM2012    object
    dtype: object




```python
lyon_UA2012[['CODE2012', 'ITEM2012']] = lyon_UA2012[['CODE2012', 'ITEM2012']].astype('category')
```

From Pandas' documentation:
> Categoricals are a pandas data type corresponding to categorical variables in statistics. A categorical variable takes on a limited, and usually fixed, number of possible values (categories; levels in R). Examples are gender, social class, blood type, country affiliation, observation time or rating via Likert scales.

Also we can look at the global distribution of the geographic types over all the urban area:

```python
total_areas = pd.merge(lyon_UA2012[['CODE2012', 'Shape_Area']].groupby('CODE2012').sum().sort_values(
    by='Shape_Area', ascending=False), codes, left_index=True, right_on='CODE2012', how='left').reset_index(drop=True)
```


```python
ax = total_areas.plot.barh(x='ITEM2012', y='Shape_Area', logx=True, figsize=figsize_S, legend=False, title='Total area per geographic type');
ax.set_xlabel('Area (km2), log scale');
plt.gca().invert_yaxis()
```


![png](../../img/2019/07/output_34_0.jpg)




Or, we can look at the spatial distribution:

```python
glasbey = ListedColormap(cc.glasbey)
lyon_UA2012.plot(figsize=figsize_L, column='ITEM2012', cmap=glasbey, legend=True, legend_kwds={'bbox_to_anchor': (1.7, 1.0), 'title': 'Geographic type'});
plt.axis('off');
```


![png](../../img/2019/07/output_35_0.jpg)

Let us just select a few of all the geographic types, in order exhibit the vegetation or water areas


```python
types = ['Forests', 'Water', 'Arable land (annual crops)', 'Pastures', 'Permanent crops (vineyards, fruit trees, olive groves)']
ax = lyon_UA2012[lyon_UA2012.ITEM2012.isin(types)].plot(
    figsize=figsize_L, column='ITEM2012', 
    cmap='tab10', legend=True, legend_kwds={'bbox_to_anchor': (1.7, 1.0), 'title': 'Geographic type'});
add_basemap(ax, url='http://tile.stamen.com/toner-background/tileZ/tileX/tileY.png', zoom=10);
plt.axis('off');
```


![png](../../img/2019/07/output_36_0.jpg)


Now we are going to compute and plot the population density. 

## Population density

Total population:


```python
lyon_UA2012.Pop2012.sum()
```




    1897722



Total area ($m^2$):


```python
lyon_UA2012.Shape_Area.sum()
```




    3669727106.711693




```python
pop_dens = 1e6 * lyon_UA2012.Pop2012.sum() / lyon_UA2012.Shape_Area.sum()
pop_dens
```




    517.1289158066248



In order to create a choropleth map, we first compute the density in number of inhabitants per $km^2$:


```python
lyon_UA2012['density'] = 1e6 * lyon_UA2012.Pop2012 / lyon_UA2012.Shape_Area
```


```python
fire = ListedColormap(cc.fire)
ax = lyon_UA2012.plot(
    column='density', figsize=figsize_L, 
    scheme='fisherjenkssampled', k=20, cmap=fire, legend=True,
    legend_kwds={'bbox_to_anchor': (1.3, 1.0), 'title': 'Population density (pop./km2)'});
add_basemap(ax, url='http://tile.stamen.com/toner-background/tileZ/tileX/tileY.png', zoom=10);
plt.axis('off');
```

![png](../../img/2019/07/output_31_0.jpg)

## Conclusion

GeoPandas is a really good package built on top of another great package: Pandas. It is open-source and incredibly handy. It allows you to explore/visualize/analyze geospatial data with a lot of ease, within the PyData ecosystem. 

On the downside, I would say that it may appear a little bit slow sometimes when dealing with larger datasets. From what I understand, this is something that is addressed by the geopandas-cython development branch?? Also, there is a Dask-Geopandas [initiative](https://github.com/geopandas/geopandas/wiki/Google-Summer-of-Code-2019), which sounds terrific!!