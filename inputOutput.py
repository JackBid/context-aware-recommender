import pandas as pd

class IO:

    def __init__(self, recommender):
        super().__init__()
        self.recommender = recommender

    # Get a user ID and confirm it exists in our dataset
    def getUserID(self):
        print('Enter user ID:')
        userID = input()

        if userID not in list(self.recommender.rawData['UserID']):
            print('No user with that ID found.')
            self.getUserID()

        return userID
    
    #Get a user ID and confirm it exists in our dataset
    def getItemID(self):
        print('Enter item ID:')
        itemID = input()

        try:
            itemID_int = int(itemID)
        except:
            print('Item ID must be an integer.')
            self.getItemID()

        if itemID_int not in list(self.recommender.rawData['ItemID']):
            print('No item with that ID found.')
            self.getItemID()

        return itemID_int

    # Get an ratings from the user - int between 1-5
    def getRating(self):
        print('Enter a rating between 1-5:')
        rating = input()

        try: 
            rating_int = int(rating)
        except:
            print('Rating must be an integer.')
            self.getRating()
        
        if rating_int < 1 or rating_int > 5:
            print('Rating must be between 1-5.')
            self.getRating

        return rating_int
    
    # Get a list of ratings from a user
    def getRatings(self, userID):

        ratings = []

        done = False

        while not done:
            itemID = self.getItemID()
            rating = self.getRating()
            tripType = self.getTripType().upper()

            ratings.append(pd.Series([userID, itemID, rating, '', '', '', '', '', tripType]))

            print('Would you like to enter another rating? (y/n)')
            another = input()

            if another.lower() != 'y':
                done = True

        return ratings

    # Get a trip type from the user - family, solo, business, couples, friends
    def getTripType(self):
        print('Enter a trip type (family, solo, business, couples, friends)')
        tripType = input()

        if tripType.lower() == 'family' or tripType.lower() == 'solo' or tripType.lower() == 'business' or tripType.lower() == 'couples' or tripType.lower() == 'friends':
            return tripType
        else:
            self.getTripType()

    
