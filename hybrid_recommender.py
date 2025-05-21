import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from content_based import get_recommendations as content_recs
from collaborative_filtering import get_top_n, model, trainset
from surprise import Dataset
from collections import defaultdict

# Load movies dataset
movies = pd.read_csv('data/movies.csv')

# Create a reverse mapping of movieId to title
movie_id_to_title = pd.Series(movies.title.values, index=movies.movieId).to_dict()

# Generate collaborative filtering predictions
print("Training collaborative filtering model (SVD)...")
predictions = model.test(trainset.build_testset())
top_n = get_top_n(predictions, n=10)

# Function to normalize a list of scores
def normalize(scores):
   
    if scores is None:
        return []
    if hasattr(scores, "empty") and scores.empty:
        return []
    if isinstance(scores, (list, tuple)) and len(scores) == 0:
        return []

    scaler = MinMaxScaler()
    if hasattr(scores, "values"):
        data = scores.values.reshape(-1, 1)
    else:
        data = [[s] for s in scores]

    return scaler.fit_transform(data).flatten().tolist()


# Function to combine recommendations
def hybrid_recommendations(user_id, favorite_movie_title, content_weight=0.5, collab_weight=0.5): 
    content_titles = content_recs(favorite_movie_title)
    print("Content titles:", content_titles)  # Debug print

    content_scores = [10 - i for i in range(len(content_titles))]
    content_scores = normalize(content_scores)
    
    content_df = pd.DataFrame({
        'title': content_titles,
        'content_score': content_scores
    })

    collab_movies = top_n.get(str(user_id), [])
    collab_df = pd.DataFrame(collab_movies, columns=['movieId', 'collab_score'])
    collab_df['title'] = collab_df['movieId'].map(movie_id_to_title)
    print("Collaborative DF titles:", collab_df['title'].tolist())  # Debug print
    
    collab_df = collab_df.dropna()
    collab_df['collab_score'] = normalize(collab_df['collab_score'])

    hybrid_df = pd.merge(content_df, collab_df, on='title', how='outer').fillna(0)
    hybrid_df['final_score'] = (hybrid_df['content_score'] * content_weight +
                                hybrid_df['collab_score'] * collab_weight)
    hybrid_df = hybrid_df.sort_values(by='final_score', ascending=False)
    
    print("Hybrid DF titles:", hybrid_df['title'].tolist())  # Debug print

    
    hybrid_df = hybrid_df[hybrid_df['title'] != "Movie not found in the dataset."]

    return hybrid_df[['title', 'final_score']].head(10)


# Example usage
if __name__ == '__main__':
    user_id = 196  # Example user from dataset
    fav_movie = 'Toy Story (1995)'
    recommendations = hybrid_recommendations(user_id, fav_movie)
    print(f"\nHybrid Recommendations for user {user_id} based on '{fav_movie}':")
    for i, row in recommendations.iterrows():
        print(f"{row['title']} (Score: {row['final_score']:.2f})")