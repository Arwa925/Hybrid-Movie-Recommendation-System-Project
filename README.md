# Collaborative Filtering Module

This module implements collaborative filtering using **SVD (Singular Value Decomposition)** from the `Surprise` library. It uses the MovieLens 100K dataset to predict user ratings and generate movie recommendations.

## Features

- Uses the built-in MovieLens 100K dataset
- Trains an SVD model on user-item interactions
- Evaluates using RMSE and MAE
- Provides top-N recommendations for each user

## Dataset

The MovieLens 100K dataset is automatically downloaded by the Surprise library.

## Output

- **RMSE** and **MAE** printed to console
- Top 5 recommended movies for a sample user


