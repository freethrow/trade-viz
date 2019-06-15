# utilities.py

# Here we define all the functions needed to pull the data
import pandas as pd

# the data
commerce = pd.read_csv('test2.csv', sep=';');

# extract the distinct values - countries and categories

all_countries = commerce.country.unique()
#print(countries)

all_categories = commerce.category.unique()
#print(categories)

# 1. top N countries for a given year, sector and N number + rest

def top_N_countries(N=10, category = 'All', year = 2018, flux = 'exchange'):

    if category =='All':
    
        data = commerce[commerce['year']==year].groupby(['country'])[flux].sum().sort_values(ascending=False).head(N)
        total = commerce[commerce['year']==year][flux].sum()
    else:

        data = commerce[(commerce['year']==year) & (commerce['category'] == category)].groupby(['country'])[flux].sum().sort_values(ascending=False).head(N)
        total = commerce[(commerce['year']==year) & (commerce['category'] == category)][flux].sum()

        
    # the amount to be appended - the total minus the top N
    to_add=pd.Series({'Rest':float(total-data.sum())})
    
    final_data = data.append(to_add)
    #print(final_data)
    
    return final_data





# now we should have the elements to compose a function that takes on some parameters
# num - the number of top sector, like 5 or 10
# the year
# the type of data: export_value, import_value or exchange
# 
def top_N_sectors(N=5, year=2018, flux='exchange', country='All'):

    if country == 'All':
        data = commerce[commerce['year']==year].groupby(['category'])[flux].sum().sort_values(ascending=False).head(N)
        total = commerce[commerce['year']==year][flux].sum()

    else:
        data = commerce[(commerce['year']==year)&(commerce['country']==country)].groupby(['category'])[flux].sum().sort_values(ascending=False).head(N)
        # the total for the year, disregarding category, but with regards to the country!
        total = commerce[(commerce['year']==year)&(commerce['country']==country)][flux].sum()
    
    # the amount to be appended
    to_add=pd.Series({'Rest':float(total-data.sum())})
    
    final_data = data.append(to_add)
    
    return final_data



# 2. for a given CATEGORY and list of COUNTRIES give us the yearly data series

# 'data': [
#   {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#   {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},]
# this is the format plotly expects - a list of dictionaries

def series_countries_per_category(countries, data_type, category, type='line'):
    
    series_list = []
    
    for country in countries:

        if country == 'All':
            if category == 'All':
                ser = commerce.groupby(['year'])[data_type].sum()
            else:
                ser = commerce[commerce['category']==category].groupby(['year'])[data_type].sum()
        else:
            if category == 'All':
                ser = commerce[commerce['country']==country].groupby(['year'])[data_type].sum()
            else:
                ser = commerce[(commerce['country']==country) & (commerce['category']==category)].groupby(['year'])[data_type].sum()
            
        series_list.append(ser)
     
    #print("Series list:", series_list)

    inter_data = pd.concat(series_list, axis=1)
    inter_data.columns = countries
    data_list = []

    

    for cnt in inter_data.columns:
    
        dct={}
        dct['x']=list(inter_data.index)
        dct['y']=list(inter_data[cnt])
        dct['type'] = type
        dct['name'] = str(cnt)

        data_list.append(dct)

        #print(data_list)

    cntr_string = '-'.join(countries)
    if data_type=='export_value':

        legend = 'Serbian export in selected countries ({} - values in 000 USD)'.format(cntr_string)
    elif data_type=='import_value':
        legend = 'Serbian import from selected countries ({} - values in 000 USD)'.format(cntr_string)
    else:
        legend = 'Serbian trade with selected countries ({} - values in 000 USD)'.format(cntr_string)


    return (data_list,legend)


# For the map we need the data from ALL the countries CODE, COUNTRY and VALUE for a given CATEGORY, YEAR and FLUX

def data_mapper(flux='exchange', year=2018, category='All'):

    if category =='All':    
        data = commerce[commerce['year']==year].groupby(['country','ccode'])[flux].sum()
        
    else:
        data = commerce[(commerce['year']==year) & (commerce['category'] == category)].groupby(['country','ccode'])[flux].sum()
    
    d = pd.DataFrame(data)
    d.reset_index(inplace=True)
    return(d)




