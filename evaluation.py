from recommender import Recommender

recommender = Recommender()

def mean_absolute_error():

    totalEntries = recommender.rawData.shape[0]

    sum_of_differences = 0
    t = 0

    for i in range(0, totalEntries, int(totalEntries/1000)):

        row = recommender.rawData.iloc[i]

        userID = row['UserID']
        itemID = row['ItemID']

        actualRating = row['Rating']

        predictedRating = recommender.predictRating(userID, itemID)

        sum_of_differences += abs(predictedRating - actualRating)

        t += 1

    return 1/t * sum_of_differences

def usage_prediction():

    user_with_most_ratings = recommender.rawData['UserID'].value_counts().index[0]
    actual_ratings = recommender.rawData[ recommender.rawData['UserID'] == user_with_most_ratings ]
    
    drop_counter = 0
    for index, values in actual_ratings.T.iteritems():
        if drop_counter % 5 == 0:
            recommender.rawData = recommender.rawData.drop([index])
        drop_counter += 1

    actual_items = list(actual_ratings['ItemID'])

    print('Pre processing data...')
    recommender.preProcessData()
    print('Calculating cosine similarity...')
    recommender.cosine_similarity()

    recs = recommender.getRecommendations(user_with_most_ratings)
    print(recs)
    
    tp = 0
    fp = 0

    for rec in recs:
        if rec in actual_items:
            tp += 1
        else:
            fp += 1


    print('tp: ' + str(tp))
    print('fp: ' + str(fp))
    

usage_prediction()