import streamlit as st
import pandas as pd
from recommender import recommend, df  # Or adjust this import if your structure is different

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")
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
    cols = st.columns(5)  # Show 2 rows of 5 posters each
    for idx, (title, rating, poster_path) in enumerate(results):
        col = cols[idx % 5]  # Rotate across 5 columns
        with col:
            if poster_path:
                full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                st.image(full_url, use_column_width=True)
            st.markdown(f"**{title}**  ⭐ {rating}")
else:
    st.warning("No good matches found.")
