import math
import numpy as np
import pandas as pd 

user = '73BED0524191DFB94AB901D12413517F'
item = 93593
item2 = 100507

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


df = pd.read_csv('res/data.csv')
item_rating_matrix = pd.pivot_table(df, index='ItemID', columns='UserID', values='Rating')

s = cosine_similarity(item_rating_matrix.loc[item], item_rating_matrix.loc[item2])
print(s)


