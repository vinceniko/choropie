<img src="https://user-images.githubusercontent.com/30331170/33049757-81c16598-ce2f-11e7-8058-8852a09c7373.png" width="30%"/>

ChoroPie
===============================

version number: 0.0.1
author: Vincent Nikolayev

Overview
--------

A Basemap/Matplotlib toolkit which allows the simplified creation of choropleth maps with colorbars using shapefiles, and the combined plotting of pie charts within the centroid coordinates of the shapefile's polygons.

#### Features:
  *Easy choropleth mapping.  
  *Easy colorbar insertion.  
  *Plot pie charts at each shp file polygon centroid.  
  *Visualize extra features using the size of the pie charts, or even size of each pie slice (ie. the length of its radius).  
  *Limit main axes limits to specific areas (zoom to areas).  
  *Translate polygons and pie charts with the geographic coordinate system.  
  *Use offsets on polygons to make slight translations.  
  *Basemap class inheritance.  
  *Access matplotlib objects.  

Example:
--------
Without size_data:  
<img src="https://user-images.githubusercontent.com/30331170/33050049-ebfc0cd2-ce30-11e7-92df-84269f423ea8.png" width="60%" />

With size_data:  
<img src="https://user-images.githubusercontent.com/30331170/33052907-04c44316-ce3f-11e7-9bb0-d3c426502de4.png" width="60%" />

With size_data and size_ratios:  
<img src="https://user-images.githubusercontent.com/30331170/33050018-b200156e-ce30-11e7-9ffa-b58885df2062.png" width="60%"/>

Installation
--------------------

To install use pip:

    $ pip install choropie


Or clone the repo:

    $ git clone https://github.com/vinceniko/choropie.git
    $ python setup.py install
    
Basic Usage
------------------
This example uses data taken from <https://www.kaggle.com/the-guardian/the-counted> and US census data including: population per state, the populations of each race in each state.  
*Disclaimer: The colors used to present the racially focused data is not reflective of any kind of idealogy. I realize that some may find the use of these colors to be offensive, but no offense was implied or intended. The chosen colors are merely used to better explain the concepts being introduced in the explanation below. 

### Code:
```
from choropie import ChoroPie as cp
basemap = dict(
    basemap_kwargs=dict(
        llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49, projection='lcc', lat_1=33, lat_2=45, lon_0=-95
    ),
    shp_file='Data/cb_2016_us_state_500k/cb_2016_us_state_500k',
    shp_key='NAME',
    figsize=(22, 12),
    )

choro = dict(
    num_colors=8,
    cmap='hot_r',
    color_data=df_state['counts'],
    )

pie = dict(
    size_data=df_state['per_capita'],
    size_ratios=df_race['per capita'],
    pie_data=df_race['percs'],
    pie_dict={'Asian': 'yellow', 'Black': 'black', 'Hispanic': 'brown',
              'Native American': 'red', 'Ocean Pacific': 'purple', 'White': 'white'},
    scale_factor_size=1,
    scale_factor_ratios=1/2
    )

test = cp.ChoroPie(**basemap)

test.choro_plot(**choro)
test.pie_plot(**pie)

test.insert_colorbar(colorbar_title='Map: Count of Killings', colorbar_loc_kwargs=dict(location='right'))
test.insert_pie_legend(legend_loc='lower right', pie_legend_kwargs=dict(title='Pies: Racial Breakdown'))
```
### Arguments Explained:
Where color_data and size data are Pandas single-index series with the area_names used in the shp file as the index.  
Ie.  

area_name | per capita rate
--- | ---
alabama | .000010
alaska | .000020
arizona | .000017

Where pie_data and size_ratios are Pandas multi-index series with the area_names used in the shp file as the first index, and the pie chart slices (the ones passed into the pie_dict parameter), as the second index. 
Ie.

area_name | race | per-race rate
--- | --- | ---
alabama | black | 0.000919
alabama | white | 0.000188
alaska | black | 0.000338
alaska | native american | 0.001135
alaska | white | 0.000105

##### Notes-   
*Pie plotting is optional. If pies are plotted, both size_data and size_ratios are optional. Not all pies have to be plotted as well (if it gets too cluttered...though in that case you can call the zoom_to_area method).  
*Choropleth plotting is optional.  
*The pie_dict parameter selects the colors for each pie slice.  
scale_factor_size and scale_fractor_ratios modify the difference in size between each pie chart and pie slice. 
*After calling zoom_to_area (which sets the limits of the main axis to the max and min of the passed in areas), call zoom_home to restore axis to original limits.  
*Other arguments should be known to matplotlib and basemap users.  

### Explanation:
size_data is a feature which can scale each pie chart's overall diameter relative to other pie charts.  
size_ratios scales the size of a slice (or the length of its radius) relative to other pie slices within the chart.  

### Results:
<img src="https://user-images.githubusercontent.com/30331170/33050018-b200156e-ce30-11e7-9ffa-b58885df2062.png" width="75%"/>

By examining these results we can see that:
1. California has had the most police killings.  
2. California has not had the highest per capita rate of police killings, with states such as New Mexico edging out ahead.  
3. In most states, the race with the most deaths were whites.  
4. Despite that, in states such as Oklahoma and Missiori, more blacks were killed proportionally when adjusted for the population differences of each race.  
