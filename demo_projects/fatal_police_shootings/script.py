import numpy as np
import pandas as pd
import os
import datetime as dt
from choropie import ChoroPie as cp

# state names and abbreviations
dict_states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

# import general state population dataset and remove first three rows
df_pop = pd.read_excel('Data/state_population_estimates.xlsx', skiprows=3)

# to remove '.' in front of state in df_pop


def remove_period(x):
    if isinstance(x, str) and x[0] == '.':
        x = x.replace('.', '')
        return x


df_pop.iloc[:, 0] = df_pop.iloc[:, 0].apply(
    remove_period)  # perform remove_period

# select necessary state rows and correct year
series_pop = df_pop.set_index(df_pop.columns[0]).loc['Alabama':'Wyoming', 2016]
series_pop.name = 'population'

# import police killings dataset
# set proper encoding or get error.
df_killings = pd.read_csv('Data/PoliceKillingsUS.csv', encoding="latin1")

# replace race abbreviations


def spam(x):
    try:
        if x[0] == 'A':
            return "Asian"
        if x[0] == 'B':
            return "Black"
        if x[0] == 'H':
            return "Hispanic"
        if x[0] == 'N':
            return "Native American"
        if x[0] == 'O':
            return "Ocean Pacific"
        if x[0] == 'W':
            return "White"
    except Exception:
        return None


df_killings['race'] = df_killings['race'].apply(spam)

# use datetime module to extract min and max dates of dataset
# format dates to Jan. 01, 06 format
# used for title of plot
max_date = df_killings['date'].apply(
    lambda x: dt.datetime.strptime(x, '%d/%m/%y')).max().strftime('%b. %d, %y')
min_date = df_killings['date'].apply(
    lambda x: dt.datetime.strptime(x, '%d/%m/%y')).min().strftime('%b. %d, %y')

# series breaking down count of killings by state
series_state = df_killings.groupby('state').count()['id']
series_state.rename('counts', inplace=True)
# series breaking down count of killings by state and race (MultiIndex)
series_race = df_killings.groupby(['state', 'race']).count()['id']

# percentage of each race killed by state
series_state_crime_race_percs = series_race / \
    series_race.groupby('state').sum() * 100


def set_index_states(df):
    if isinstance(df.index, pd.MultiIndex):
        list_abb = [dict_states[abb] for abb in df.index.levels[0]]
        df.index.set_levels(list_abb, level=0, inplace=True)
    elif isinstance(df.index, pd.Index):
        list_abb = [dict_states[abb] for abb in df.index]
        df.index = list_abb


# fix indexes (replace state abbreviations with state name)
# series_race and series_state
set_index_states(series_race)
set_index_states(series_state)

df_state = pd.concat([series_state, series_pop], axis=1)

# per capita percentage
df_state['per_capita'] = df_state['counts'] / df_state['population']

# population by race for each state
df_state_race = pd.read_excel('Data/state_race.xlsx', index_col=0)

df_state_race = df_state_race.iloc[1:, :]
df_state_race.columns.name = 'race'

df_massaged = pd.melt(df_state_race.reset_index(),
                      id_vars='Geography', value_vars=df_state_race.columns)
df_massaged = df_massaged.groupby(
    ['Geography', 'race']).agg(lambda x: x.iloc[0])

df_race = pd.concat([series_race, series_state_crime_race_percs,
                     df_massaged], axis=1).dropna()
df_race.columns = ['count', 'percs', 'pop']
df_race['per_capita'] = df_race['count'] / df_race['pop']

###################

# df_state.drop('California', inplace=True)

###
shp_file = 'Data/cb_2016_us_state_500k/cb_2016_us_state_500k'

shp_lst = cp.get_shp_attributes(shp_file)
shp_key = cp.find_shp_key(df_state['counts'].index, shp_lst)
###

basemap = dict(
    basemap_kwargs=dict(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64,
                        urcrnrlat=49, projection='lcc', lat_1=33, lat_2=45, lon_0=-95),
    shp_file=shp_file,
    shp_key=shp_key,
    figsize=(22, 12),
)

choro = dict(
    num_colors=8,
    cmap='hot_r',
    color_data=df_state['counts'],
)

pie = dict(
    size_data=df_state['per_capita'],
    size_ratios=df_race['per_capita'],
    pie_data=df_race['percs'],
    pie_dict={'Asian': 'yellow', 'Black': 'black', 'Hispanic': 'brown',
              'Native American': 'red', 'Ocean Pacific': 'purple', 'White': 'white'},
    scale_factor_size=1,
    scale_factor_ratios=1 / 2
)

test = cp.ChoroPie(**basemap)

test.clear_elements()

test.choro_plot(**choro)
test.pie_plot(**pie)

test.insert_colorbar(colorbar_title='Map: Count of Killings',
                     colorbar_loc_kwargs=dict(location='right'))
test.insert_pie_legend(legend_loc='lower right',
                       pie_legend_kwargs=dict(title='Pies: Racial Breakdown'))

test.ax.set_title('Police Killings: Jan. 02, 15 - Jul. 31, 17\nTotal: {:,d}'.format(
    df_killings.iloc[:, 0].count()), fontsize=35, fontweight='bold', x=0.61, y=0.90)

test.fig.savefig('Outputs/qwerty.png', bbox_inches='tight')

test.ax_colorbar.set_yticklabels(['{:.0f}'.format(
    float(i.get_text())) for i in test.ax_colorbar.get_ymajorticklabels()])

# for i, j in test.corr_centroids.items():
#     if i in series_state:
#         test.ax.text(*j, i, fontsize=15, color='red')

# test.zoom_to_area('New York')
test.fig
