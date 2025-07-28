import streamlit as st
import pandas as pd
from recommender import recommend, df  # Or adjust this import if your structure is different

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Sam's Recommendation ")
st.markdown("Find similar movies based on content and ratings!")

# Dropdown list of movie titles
movie_list = df['title'].sort_values().unique()
selected_movie = st.selectbox("Pick a movie", movie_list)

# Recommend button
if st.button("Recommend"):
    st.subheader(f"📽️ Top Recommendations for: {selected_movie}")
    results = recommend(selected_movie)
    
    if results:
        for title, rating in results:
            st.markdown(f"**{title}**  ⭐ {rating}")
    else:
        st.warning("No good matches found.")

results = recommend(selected_movie)

if results:
    num_columns = 5
    for row_start in range(0, len(results), num_columns):
        cols = st.columns(num_columns)
        for idx in range(num_columns):
            if row_start + idx < len(results):
                title, rating, poster_path = results[row_start + idx]
                with cols[idx]:
                    if poster_path:
                        full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                        st.image(full_url, use_container_width=True)
                    st.markdown(f"**{title}**  ⭐ {rating}")
else:
    st.warning("No good matches found.")
