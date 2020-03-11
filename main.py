import math
import numpy as np
import pandas as pd 
import operator
import random

user = '73BED0524191DFB94AB901D12413517F'
item = 93593
item2 = 100507

# Find items similar to a particular item
def findSimilarItems(item):
    simiarities = []
    
    for index, row in user_item_matrix.iterrows():
        if index == item: continue
        simiarities.append((index, cosine_similarity(user_item_matrix.loc[item], user_item_matrix.loc[index])))

    return simiarities

# Find the cosine similarity between two items, i1 and i2
def cosine_similarity(i1, i2):
    
    # Convert to array and remove nan values
    np_i1 = i1.to_numpy()
    np_i2 = i2.to_numpy()

    np_i1[np.isnan(np_i1)] = 0
    np_i2[np.isnan(np_i2)] = 0

    # Calculate the squared sums of np_i1 and np_i2
    squarer = lambda t: t ** 2
    vfunc = np.vectorize(squarer)

    i1_squared_sum = sum(vfunc(np_i1))
    i2_squared_sum = sum(vfunc(np_i2))

    # Apple cosine similarity function
    similarity = 0
    for i in range(len(np_i1)):
        similarity += (np_i1[i] * np_i2[i]) / (math.sqrt(i1_squared_sum) * math.sqrt(i2_squared_sum))

    return similarity

def readData():
    n = 14176 #number of records in file
    s = 14000 #desired sample size
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

    result = pd.pivot_table(result, index='ItemID', columns='UserID', values='Rating').fillna(0)

    return result


rawData = readData()
user_item_matrix = preProcessData(rawData)


s = findSimilarItems(224311)
s.sort(key=operator.itemgetter(1), reverse=True)
s = s[:10]
print(s)






