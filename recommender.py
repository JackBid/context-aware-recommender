import math
import operator
import random

import numpy as np
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity

class Recommender():

    def __init__(self):
        super().__init__()

        print('Pre processing data...')
        self.preProcessData()
        print('Calculating cosine similarity...')
        self.cosine_similarity()

    # Read the data from the file
    def readData(self):
        n = 14176 #number of records in file
        s = 14176 #desired sample size
        filename = "res/data.csv"
        skip = sorted(random.sample(range(n),n-s))

        if 0 in skip:
            skip.remove(0)
        return pd.read_csv(filename, skiprows=skip)

    def find_n_neighbours(self, df,n):
        order = np.argsort(df.values, axis=1)[:, :n]
        df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
            .iloc[:n].index, 
            index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
        return df

    # Calculate the contextual probability between users given a trip type
    def contextual_probability(self, user1, user2, trip_type):

        numberUser2Ratings = len(self.rawData[self.rawData['UserID'] == user2])
        numberUSer2RatingsSameContext = len(self.rawData[ (self.rawData['UserID'] == user2) & (self.rawData['TripType'] == trip_type) ])

        return numberUSer2RatingsSameContext / numberUser2Ratings

    # Take the list of the top similar users and reorder based on context
    def filter_similar_users_for_context(self, user):

        similar_users = self.similarity_30.loc[user]

        similarities = []
        context = []
        scores = []

        user_context = pd.DataFrame(self.rawData.groupby('UserID')['TripType'].agg(lambda x:x.value_counts().index[0])).loc[user].get('TripType')

        for index, value in similar_users.iteritems():
            similarities.append(self.similarity.at[user, value])
            context.append(self.contextual_probability(user, value, user_context))

        similar_users = pd.DataFrame(similar_users)
        similar_users['similarities'] = similarities
        similar_users['context'] = context

        similar_users['final_score'] = similar_users['similarities'] * similar_users['context']

        similar_users = similar_users.sort_values(by=['final_score'], ascending=False)
        
        return similar_users

    def get_items_from_users(self, users):

        itemIDs = []
        
        for index, value in users.iteritems():
            query = self.rawData[ (self.rawData['UserID'] ==  value) & (self.rawData['Rating'] == 5) ]
            if len(query) > 0:
                itemIDs.append(query.iloc[0]['ItemID'])
            if len(query) > 1:
                itemIDs.append(query.iloc[1]['ItemID'])
            #itemIDS.append(rawData[ (rawData['UserID'] ==  value) & (rawData['Rating'] == 5) ])

        return itemIDs

    def user_item_score(self, user,item):
        a = similarity_30[similarity_30.index==user].values
        b = a.squeeze().tolist()
        c = final_item.loc[:,item]
        d = c[c.index.isin(b)]
        f = d[d.notnull()]
        avg_user = mean.loc[mean['UserID'] == user,'Rating'].values[0]
        index = f.index.values.squeeze().tolist()
        corr = similarity.loc[user,index]
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ['adg_score','correlation']
        fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
        nume = fin['score'].sum()
        deno = fin['correlation'].sum()
        final_score = avg_user + (nume/deno)
        return final_score


    def preProcessData(self):
        self.rawData = self.readData()

        # Find the mean rating for each user
        self.mean = self.rawData.groupby(by='UserID', as_index=False)['Rating'].mean()

        # Calculate normalised rating for each user which is the original rating - the average rating of that user
        self.rating_norm = pd.merge(self.rawData, self.mean, on='UserID')
        self.rating_norm['rating_norm'] = self.rating_norm['Rating_x'] - self.rating_norm['Rating_y']

        # Create user item matrix
        self.user_item_matrix = pd.pivot_table(self.rating_norm, index='UserID', columns='ItemID', values='rating_norm')

        # Replace NaN by item average
        self.final_item = self.user_item_matrix.fillna(self.user_item_matrix.mean(axis=0))

        # Replace NaN by user average
        self.final_user = self.user_item_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)

    def cosine_similarity(self):
        # Calculate cosine similarity
        cosine = cosine_similarity(self.final_item)
        np.fill_diagonal(cosine, 0)
        self.similarity = pd.DataFrame(cosine, index=self.final_item.index)
        self.similarity.columns = self.final_user.index

        #Top 30 neighbours for each user
        self.similarity_30 = self.find_n_neighbours(self.similarity, 30)

    def getRecommendations(self, user):
        similar_users = self.filter_similar_users_for_context(user).reset_index()[user].head()
        recs = self.get_items_from_users(similar_users)
        print(recs)

    def predictRating(user, item):
        print(user_item_score(user, item))


