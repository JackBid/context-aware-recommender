import numpy as np
import pandas as pd 

d = pd.read_csv('res/listening_data.txt', sep='\t', names=['twitter-id', 'user-id', 'month', 'weekday', 'longitude', 'latitude', 'country-id', 'city-id', 'artist-id', 'track-id'])
print(d.head())
