import streamlit as st
import pandas as pd
from difflib import get_close_matches
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

import os
API_KEY = st.secrets["TMDB_API_KEY"]

def get_poster(movie_title):
	clean_title = re.sub(r"\(\d{4}\)", "", movie_title).strip()	

	url = f"https://api.themoviedb.org/3/search/movie?	api_key={API_KEY}&query={clean_title}"
	data = requests.get(url).json()

	if data["results"]:
		for result in date["results"]:
			if result["poster_path"]:
				return "https://image.tmdb.org/t/p/w500" + result["poster_path"]

if poster:
	st.image(poster)
else:
	st.image("https://via.placeholder.com/300x450?text=No+Image")

return None

st.title("Movie Recommender")
st.caption("Type a movie you like and get recommendations 🎥🍿")

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

titles = movies["title"].tolist()

movies["genres"] = movies["genres"].str.replace("|", " ")
vectorizer = CountVectorizer()
genre_matrix = vectorizer.fit_transform(movies["genres"])
content_similarity = cosine_similarity(genre_matrix)

def recommend(movie_title):
	matches = get_close_matches(movie_title, titles, n=1, cutoff=0.4)

	if not matches:	
		return ["Movie not found"]

	best_match = matches[0]

	idx = movies[movies["title"] == best_match].index[0]

	scores = list(enumerate(content_similarity[idx]))
	scores = sorted(scores, key=lambda x: x[1], reverse=True)

	recommendations = []
	for i in scores[1:6]:
		recommendations.append(movies.iloc[i[0]]["title"])

	return [best_match] + recommendations

user_input = st.selectbox("Choose a movie:", titles)

if st.button("Recommend"):
	results = recommend(user_input)

	st.write(f"### Showing results for: {results[0]}")

	for movie in results[1:]:
		poster = get_poster(movie)

		if poster:
			st.image(poster, width=150)
		st.write(movie)