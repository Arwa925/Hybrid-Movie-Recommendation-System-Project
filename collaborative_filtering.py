from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split
from collections import defaultdict

data = Dataset.load_builtin('ml-100k')
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

model = SVD()
model.fit(trainset)
predictions = model.test(testset)

print("Evaluation Metrics:")
accuracy.rmse(predictions)
accuracy.mae(predictions)

def get_top_n(preds, n=5):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in preds:
        top_n[uid].append((iid, est))
    for uid in top_n:
        top_n[uid] = sorted(top_n[uid], key=lambda x: x[1], reverse=True)[:n]
    return top_n

top_recommendations = get_top_n(predictions, n=5)
sample_user = next(iter(top_recommendations))
print(f"\nTop 5 recommendations for user {sample_user}:")
for movie_id, predicted_rating in top_recommendations[sample_user]:
    print(f"Movie ID: {movie_id}, Predicted Rating: {predicted_rating:.2f}")
