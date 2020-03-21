from recommender import Recommender

recommender = Recommender()

def mean_absolute_error():

    totalEntries = recommender.rawData.shape[0]

    sum_of_differences = 0
    t = 0
    '''
    for i in range(0, totalEntries, int(totalEntries/1000)):

        row = recommender.rawData.iloc[i]

        userID = row['UserID']
        itemID = row['ItemID']

        actualRating = row['Rating']

        predictedRating = recommender.predictRating(userID, itemID)

        sum_of_differences += abs(predictedRating - actualRating)

        t += 1'''
    
    for i in range(0, 14000):

        row = recommender.rawData.iloc[i]

        if row['Rating'] == 5:

            userID = row['UserID']
            itemID = row['ItemID']

            actualRating = row['Rating']

            predictedRating = recommender.predictRating(userID, itemID)
            if predictedRating > 5:
                predictedRating = 5

            #print(actualRating)
            #print(predictedRating)
            #print()

            sum_of_differences += abs(predictedRating - actualRating)

            t += 1

    return 1/t * sum_of_differences

def usage_prediction_values():

    # Find user with most ratings
    user_with_most_ratings = recommender.rawData['UserID'].value_counts().index[0]
    actual_ratings = recommender.rawData[ recommender.rawData['UserID'] == user_with_most_ratings ]
    
    # Remove 1/3 if users ratings
    drop_counter = 0
    for index, values in actual_ratings.T.iteritems():
        if drop_counter % 3 == 0:
            recommender.rawData = recommender.rawData.drop([index])
        drop_counter += 1

    actual_items = list(actual_ratings['ItemID'])

    # Get recommendations
    recommender.preProcessData()
    recommender.cosine_similarity()

    recs = recommender.getRecommendations(user_with_most_ratings)
    
    # usage prediction variables
    tp = 0
    fp = 0
    fn = 0

    # Calculate true positive and false positive results
    for rec in recs:
        if rec in actual_items:
            tp += 1
        else:
            fp += 1

    # Calculate false negatives
    for used in actual_items:
        if used not in recs:
            fn += 1

    return tp, fp, fn

def precision():
    tp, fp, _ = usage_prediction_values()

    return tp / (tp + fp)

def recall():
    tp, _, fn = usage_prediction_values()

    return tp / (tp + fn)

print(mean_absolute_error())
