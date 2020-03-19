from recommender import Recommender

class UI():

    def __init__(self):
        super().__init__()

        self.recommender = Recommender()
        self.menu()

    def existing_user(self):
        print('Enter user ID:')
        userID = input()

        if userID not in list(self.recommender.rawData['UserID']):
            print('No user with that ID found.')
            self.existing_user()
        
        self.recommender.getRecommendations(userID)

        return

    def menu(self):
        print('\nOptions\n 1. Build a user profile\n 2. Use an existing user\n 3. Predict a user item rating\n Enter 1, 2 or 3:')
        option = input()
        try:
            int_option = int(option)
        except:
            print(option + ' is not a number.')
            self.menu()

        if int_option == 2:
            self.existing_user()

        self.menu()

UI = UI()






