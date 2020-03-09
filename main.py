import numpy as np
import pandas as pd 

user = '73BED0524191DFB94AB901D12413517F'
item = 93593

df = pd.read_csv('res/data.csv')

item_rating_matrix = pd.pivot_table(df, index='ItemID', columns='UserID', values='Rating')

print(item_rating_matrix.loc[item][user])

