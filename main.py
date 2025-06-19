from content_based_recommender import ContentBasedRecommender

recommender = ContentBasedRecommender('movies.csv')
recommendations = recommender.get_recommendations([101, 102, 108], 5)