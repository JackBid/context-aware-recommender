import math
import numpy as np
import pandas as pd 
import operator
import random

user = '003BC319571635C677EEFC610BD066F5'
item = 81126 
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

def findSimilarItems(item):
    item_series = user_item_matrix[item]
    similar_items = user_item_matrix.corrwith(item_series, method='pearson')

    corr_similar_items = pd.DataFrame(similar_items, columns=['Correlation'])
    corr_similar_items.dropna(inplace=True)
    corr_similar_items = corr_similar_items.join(ratings_mean_count['RatingCount'])
    corr_similar_items = corr_similar_items.join(context['TripType'])
    corr_similar_items = corr_similar_items[corr_similar_items['RatingCount']>10].sort_values('Correlation', ascending=False)

    item_context = corr_similar_items.loc[item]['TripType']

    num_same_context_items = len(corr_similar_items[corr_similar_items['TripType'] == item_context])
    num_similar_items = len(corr_similar_items['Correlation'])

    corr_similar_items['Correlation'] = corr_similar_items['Correlation'] * (num_same_context_items / num_similar_items)

    return corr_similar_items.head(6)

def recommendItems(user):
    top_user_items = user_item_matrix.loc[user].sort_values(ascending=False).head(5)
    
    recs = 0
    first = True

    for index, value in top_user_items.items():
        if first:
            recs = findSimilarItems(index).drop(index)
            first = False
        else:
            recs = pd.concat([recs, findSimilarItems(index).drop(index)], ignore_index=False, sort=True)

    recs = recs.sort_values('Correlation', ascending=False).head(10)

    return recs

#def postFiltering(recs):


rawData = readData()
user_item_matrix = preProcessData(rawData)

ratings_mean_count = pd.DataFrame(rawData.groupby('ItemID')['Rating'].count().sort_values(ascending=False))
ratings_mean_count = ratings_mean_count.rename(columns = {'ItemID': 'ItemID', 'Rating':'RatingCount'})
context = pd.DataFrame(rawData.groupby('ItemID')['TripType'].agg(lambda x:x.value_counts().index[0]))

#findSimilarItems(item)

recs = recommendItems(user)

print(recs)





