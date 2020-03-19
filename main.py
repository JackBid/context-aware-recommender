import random
import string
import pandas as pd

from recommender import Recommender
from inputOutput import IO

class UI():

    def __init__(self):
        super().__init__()
        
        self.recommender = Recommender()
        self.io = IO(self.recommender)
        self.menu()

    # get recs for an existing user
    def existingUser(self):
        userID = self.io.getUserID()
        self.recommender.getRecommendations(userID)

        return

    # Get a userId and itemID from the user and find a predicited rating
    def predicitedRating(self):
        userID = self.io.getUserID()
        itemID = self.io.getItemID()

        self.recommender.predictRating(userID, itemID)

    # Create a new user id - string of numbers and letters of length 32
    def createNewUserID(self):
        userID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

        if userID in list(self.recommender.rawData['UserID']):
            self.createNewUserID
        
        return userID

    # Build a new user profile and get a rating
    def buildProfile(self):
        userID = self.createNewUserID()
        ratings = self.io.getRatings(userID)

        for rating in ratings:
            self.recommender.rawData = pd.concat([self.recommender.rawData, pd.DataFrame(rating).T.rename(columns={0:'UserID', 1:'ItemID', 2:'Rating', 3:'UserState', 4:'UserTimeZone', 5:'ItemCity', 6:'ItemState', 7:'ItemTimeZone', 8:'TripType'})])

        self.recommender.rawData = self.recommender.rawData.astype({'ItemID': int, 'Rating':int})

        print('Processing new user profile...')
        self.recommender.preProcessData()
        print('Calculating new cosine similarities...')
        self.recommender.cosine_similarity()

        self.recommender.getRecommendations(userID)

        return

    # main menu of options
    def menu(self):
        print('\nOptions\n 1. Build a user profile\n 2. Use an existing user\n 3. Predict a user item rating\n Enter 1, 2 or 3:')
        option = input()
        try:
            int_option = int(option)
        except:
            print(option + ' is not a number.')
            self.menu()
        
        if int_option == 1:
            self.buildProfile()
        elif int_option == 2:
            self.existingUser()
        elif int_option == 3:
            self.predicitedRating()

        self.menu()

UI = UI()






