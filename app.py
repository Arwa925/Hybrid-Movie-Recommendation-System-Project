import streamlit as st
from hybrid_recommender import hybrid_recommendations
import pandas as pd

movies_df = pd.read_csv("data/movies.csv")

movie_titles_list = movies_df['title'].dropna().unique().tolist()


st.title("Hybrid Movie Recommendation System")
st.markdown("Get personalized movie suggestions based on your preferences!")

option = st.radio("Choose a recommendation method:", ("By Movie Title", "By User ID"))

if option == "By Movie Title":
    user_id = st.number_input("Enter your User ID:", min_value=1, step=1)
    favorite_movie_title = st.selectbox("Select your favorite movie title:", movie_titles_list)
    
    if st.button("Get Recommendations"):
        if user_id and favorite_movie_title:
            recommendations = hybrid_recommendations(user_id=int(user_id), favorite_movie_title=favorite_movie_title)
            if isinstance(recommendations, str):
                st.warning(recommendations)
            else:
                st.subheader("Recommended Movies:")
                for idx, row in recommendations.iterrows():
                    st.write(f"{idx+1}. {row['title']} (Score: {row['final_score']:.2f})")
        else:
            st.error("Please enter both User ID and select a favorite movie.")

else:  # By User ID
    user_id = st.number_input("Enter your User ID:", min_value=1, step=1)
    favorite_movie_title = st.selectbox("Select your favorite movie title:", movie_titles_list)
    
    if st.button("Get Recommendations"):
        if user_id and favorite_movie_title:
            recommendations = hybrid_recommendations(user_id=int(user_id), favorite_movie_title=favorite_movie_title)
            if isinstance(recommendations, str):
                st.warning(recommendations)
            else:
                st.subheader("Recommended Movies:")
                for idx, row in recommendations.iterrows():
                    st.write(f"{idx+1}. {row['title']} (Score: {row['final_score']:.2f})")
        else:
            st.error("Please enter both User ID and select a favorite movie.")
