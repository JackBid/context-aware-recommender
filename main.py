import math
import numpy as np
import pandas as pd 
import operator
import random

user = '73BED0524191DFB94AB901D12413517F'
item = 93593
item2 = 100507


def readData():
    n = 14176 #number of records in file
    s = 14176 #desired sample size
    filename = "res/data.csv"
    skip = sorted(random.sample(range(n),n-s))

    if 0 in skip:
        skip.remove(0)
    return pd.read_csv(filename, skiprows=skip)

def preProcessData(rawData):
    mean = rawData.groupby(['UserID'], as_index=False, sort=False).mean().rename(columns={'UserID':'UserID', 'Rating':'Rating_mean'})

    ratings = pd.merge(rawData, mean, on='UserID', how='left', sort='False')
    ratings['rating_adjusted'] = ratings['Rating'] - ratings['Rating_mean']
    result = pd.DataFrame({'UserID': ratings['UserID'], 
                            'ItemID': ratings['ItemID_x'],
                            'Rating': ratings['Rating_mean']})

    result = pd.pivot_table(result, index='UserID', columns='ItemID', values='Rating').fillna(0)

    return result

def findSimilarItems(item, ratings_mean_count):

    item_series = user_item_matrix[item]
    similar_items = user_item_matrix.corrwith(item_series, method='pearson')

    corr_similar_items = pd.DataFrame(similar_items, columns=['Correlation'])
    corr_similar_items.dropna(inplace=True)
    #corr_similar_items = corr_similar_items.sort_values('Correlation', ascending=False).head()
    corr_similar_items = corr_similar_items.join(ratings_mean_count['RatingCount'])
    corr_similar_items = corr_similar_items[corr_similar_items['RatingCount']>10].sort_values('Correlation', ascending=False).head()
    #corr_forrest_gump[corr_forrest_gump ['rating_counts']>50].sort_values('Correlation', ascending=False).head()
    
    return corr_similar_items 

rawData = readData()
user_item_matrix = preProcessData(rawData)

ratings_mean_count = pd.DataFrame(rawData.groupby('ItemID')['Rating'].count().sort_values(ascending=False))
ratings_mean_count = ratings_mean_count.rename(columns = {'ItemID': 'ItemID', 'Rating':'RatingCount'})

users = findSimilarItems(878115, ratings_mean_count)
print(users)

'''
similarity_matrix = {}

s = findSimilarItems(user_item_matrix.iloc[0])
s.sort(key=operator.itemgetter(1), reverse=True)
s = s[:10]
print(s)
'''





