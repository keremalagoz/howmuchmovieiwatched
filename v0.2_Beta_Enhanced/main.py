from content_based_recommender import ContentBasedRecommender

recommender = ContentBasedRecommender('processed_tmdb_movies.csv')
recommendations = recommender.get_recommendations([19995, 285, 206647], 5)