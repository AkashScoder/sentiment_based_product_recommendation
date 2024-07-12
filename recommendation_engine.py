import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import cryptography
icon = Image.open(
    "C://Users//akash//PycharmProjects//PhonePe pulse visualization//Phonepe-Pulse-Data-Visualization-and-Exploration//PhonePe-IMG.jpg")
st.set_page_config(
    page_title="Phonepe Pulse Data Visualization | By Akash S",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This dashboard app is created by Akash
                        Data has been cloned from Phonepe Pulse Github Repository"""})

# Sidebar header
st.sidebar.header(" Welcome to the dashboard ")


# Step 1: Load Data from SQL
engine = create_engine('mysql+pymysql://root:2261389@localhost/recommendation')
query = "SELECT * from reviews_with_aspect_ratings"
data = pd.read_sql(query, engine)

# Normalize aspect ratings if not already normalized
features = ['Camera', 'Performance', 'Display', 'Battery', 'Design', 'value for money']
data[features] = data[features] / 5.0

# Step 2: Aggregate Sentiment Features at the Product Level
product_features = data.groupby('Name')[features].mean().reset_index()

# Define the price dictionary
product_prices = {
    'samsung-galaxy-s23': 39999,
    'poco-x3-pro': 25999,
    'oneplus-nord-ce4': 26980,
    'vivo-v30-5g': 37999,
    'apple-iphone-12': 39999,
    'motorola-edge-50-pro': 34999,
    'realme-12-pro-5g': 23999,
    'iqoo-z9-5g': 20458,
}

# Add prices to product_features DataFrame
product_features['actual_price'] = product_features['Name'].map(product_prices)

# Calculate cosine similarity between all product features
feature_matrix = product_features[features].values
similarity_matrix = cosine_similarity(feature_matrix)


# Function to parse user input and suggest a single product
def suggest_product(user_input, product_features):
    # Extract price constraint if mentioned
    min_price, max_price = None, None

    # Tokenize user input
    user_input_list = user_input.lower().split()

    # Extract price range
    for idx, word in enumerate(user_input_list):
        if word.isnumeric():
            price = int(word)
            if idx > 0 and user_input_list[idx - 1] in ['below', 'under']:
                max_price = price
            elif idx > 0 and user_input_list[idx - 1] in ['above', 'over']:
                min_price = price
            elif idx > 0 and user_input_list[idx - 1] == 'between' and len(user_input_list) > idx + 2 and \
                    user_input_list[idx + 2].isnumeric():
                min_price = price
                max_price = int(user_input_list[idx + 2])

    # Define the aspect keywords
    aspect_keywords = {
        'camera': 'Camera',
        'display': 'Display',
        'performance': 'Performance',
        'battery': 'Battery',
        'design': 'Design',
        'value': 'value for money'
    }

    # Identify the relevant feature based on user input
    relevant_features = [value for key, value in aspect_keywords.items() if key in user_input.lower()]

    if not relevant_features:
        # If no specific feature is mentioned, use overall sentiment
        relevant_features = features

    # Rank products based on the relevant feature(s)
    product_scores = product_features[['Name'] + relevant_features + ['actual_price']].copy()
    product_scores['overall_score'] = product_scores[relevant_features].mean(axis=1)

    # Filter based on price range
    if min_price is not None:
        product_scores = product_scores[product_scores['actual_price'] >= min_price]
    if max_price is not None:
        product_scores = product_scores[product_scores['actual_price'] <= max_price]

    # Recommend the top product based on the highest overall score
    if product_scores.empty:
        return "No products found within the specified price range."

    top_product = product_scores.sort_values(by='overall_score', ascending=False).head(1)['Name'].values[0]

    return top_product


# Streamlit application
st.title('Product Recommendation System')

user_prompt = st.text_input('Enter your query for product recommendation:')
if user_prompt:
    recommended_product = suggest_product(user_prompt, product_features)
    st.write("Recommended product:", recommended_product)
