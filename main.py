import math
import operator
import random

import numpy as np
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity

user = '003BC319571635C677EEFC610BD066F5'
item = 81126 
item2 = 100507

# Read the data from the file
def readData():
    n = 14176 #number of records in file
    s = 14176 #desired sample size
    filename = "res/data.csv"
    skip = sorted(random.sample(range(n),n-s))

    if 0 in skip:
        skip.remove(0)
    return pd.read_csv(filename, skiprows=skip)

# Process data so that ratings are adjusted by subtracting mean
def preProcessData(rawData):
    mean = rawData.groupby(['UserID'], as_index=False, sort=False).mean().rename(columns={'UserID':'UserID', 'Rating':'Rating_mean'})

    ratings = pd.merge(rawData, mean, on='UserID', how='left', sort='False')
    ratings['rating_adjusted'] = ratings['Rating'] - ratings['Rating_mean']
    result = pd.DataFrame({'UserID': ratings['UserID'], 
                            'ItemID': ratings['ItemID_x'],
                            'Rating': ratings['Rating_mean']})

    result = pd.pivot_table(result, index='UserID', columns='ItemID', values='Rating').fillna(0)

    return result

def get_user_similar_items(user1, user2):

    user1_ratings = rating_norm[rating_norm.UserID == user1]
    user2_ratings = rating_norm[rating_norm.UserID == user2]

    common_items = user1_ratings.merge(user2_ratings, on = 'ItemID', how = 'inner')

    return common_items.merge(rawData, on = 'ItemID')

def find_n_neighbours(df,n):
    order = np.argsort(df.values, axis=1)[:, :n]
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
           .iloc[:n].index, 
          index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
    return df

# Calculate the contextual probability between users given a trip type
def contextual_probability(user1, user2, trip_type):

    numberUser2Ratings = len(rawData[rawData['UserID'] == user2])
    numberUSer2RatingsSameContext = len(rawData[ (rawData['UserID'] == user2) & (rawData['TripType'] == trip_type) ])

    return numberUSer2RatingsSameContext / numberUser2Ratings

# Take the list of the top similar users and reorder based on context
def filter_similar_users_for_context(user, similarity):
    similar_users = similarity_30_m.loc[user]

    similarities = []
    context = []
    scores = []

    user_context = pd.DataFrame(rawData.groupby('UserID')['TripType'].agg(lambda x:x.value_counts().index[0])).loc[user].get('TripType')

    for index, value in similar_users.iteritems():
        similarities.append(similarity.at[user, value])
        context.append(contextual_probability(user, value, user_context))

    similar_users = pd.DataFrame(similar_users)
    similar_users['similarities'] = similarities
    similar_users['context'] = context

    similar_users['final_score'] = similar_users['similarities'] * similar_users['context']

    similar_users = similar_users.sort_values(by=['final_score'], ascending=False)
    
    return similar_users

def get_items_from_users(users):

    itemIDs = []
    
    for index, value in users.iteritems():
        query = rawData[ (rawData['UserID'] ==  value) & (rawData['Rating'] == 5) ]
        if len(query) > 0:
            itemIDs.append(query.iloc[0]['ItemID'])
            itemIDs.append(query.iloc[1]['ItemID'])
        #itemIDS.append(rawData[ (rawData['UserID'] ==  value) & (rawData['Rating'] == 5) ])

    return itemIDs


rawData = readData()

# Find the mean rating for each user
mean = rawData.groupby(by='UserID', as_index=False)['Rating'].mean()

# Calculate normalised rating for each user which is the original rating - the average rating of that user
rating_norm = pd.merge(rawData, mean, on='UserID')
rating_norm['rating_norm'] = rating_norm['Rating_x'] - rating_norm['Rating_y']

# Create user item matrix
user_item_matrix = pd.pivot_table(rating_norm, index='UserID', columns='ItemID', values='rating_norm')

# Replace NaN by item average
final_item = user_item_matrix.fillna(user_item_matrix.mean(axis=0))

# Replace NaN by user average
final_user = user_item_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)

# Calculate cosine similarity
cosine = cosine_similarity(final_item)
np.fill_diagonal(cosine, 0)
similarity = pd.DataFrame(cosine, index=final_item.index)
similarity.columns = final_user.index

#Top 30 neighbours for each user
similarity_30_m = find_n_neighbours(similarity, 30)

def getRecommendations(user):
    similar_users = filter_similar_users_for_context(user, similarity).reset_index()[user].head()
    recs = get_items_from_users(similar_users)
    print(recs)

getRecommendations(user)





