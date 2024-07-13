#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import pipeline
from sqlalchemy import create_engine

# Database connection
engine = create_engine('mysql+pymysql://root:2261389@localhost/recommendation')

# Ensure you have downloaded the necessary NLTK data
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Step 1: Load the Dataset
df = pd.read_sql('select * from sentiment_reviews', engine)

# Step 2: Preprocess the Reviews
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\b\w{1,2}\b', '', text)  # Remove short words
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_tokens)

df['review_cleaned'] = df['Reviews'].apply(preprocess_text)

# Step 3: Aspect-Based Sentiment Analysis (ABSA)
absa_model = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')

aspects = ['Camera', 'Display', 'Performance', 'Battery', 'Design', 'value for money']

def analyze_aspects(review, aspects):
    aspect_sentiments = {}
    for aspect in aspects:
        aspect_review = f"{aspect} {review}"
        sentiment = absa_model(aspect_review)[0]
        rating = int(sentiment['label'].split()[0])  # Convert 'label' to numerical rating
        aspect_sentiments[aspect] = rating
    return aspect_sentiments

df['aspect_ratings'] = df['review_cleaned'].apply(lambda x: analyze_aspects(x, aspects))

# Step 4: Store the Results
# Expand the dictionary into separate columns
aspect_ratings_df = df['aspect_ratings'].apply(pd.Series)

# Merge the sentiment columns with the original DataFrame
df = pd.concat([df, aspect_ratings_df], axis=1)

# Drop the aspect_ratings column as it's no longer needed
df.drop(columns=['aspect_ratings'], inplace=True)

# Save the DataFrame with the sentiment analysis results
df.to_sql(name='reviews_with_aspect_ratings',con=engine,if_exists='append',index=False)

print("Sentiment analysis completed and results saved to 'reviews_with_aspect_ratings in sql")


# In[11]:


# df[df['camera quality']>4]
df


# In[12]:


overall_ratings_list=[]


# In[16]:


def overall_rating(df, phone_name):
    overall_ratings = {}
    overall_ratings['Name'] = phone_name
    overall_ratings['Camera'] = df[df['Name'] == phone_name]['Camera'].mean()
    overall_ratings['Display'] = df[df['Name'] == phone_name]['Display'].mean()
    overall_ratings['Performance'] = df[df['Name'] == phone_name]['Performance'].mean()
    overall_ratings['Battery'] = df[df['Name'] == phone_name]['Battery'].mean()
    overall_ratings['Design'] = df[df['Name'] == phone_name]['Design'].mean()
    overall_ratings['value for money'] = df[df['Name'] == phone_name]['value for money'].mean()
    
    overall_ratings_list.append(overall_ratings)


# In[17]:


phone_list=['samsung-galaxy-s23','poco-x3-pro','oneplus-nord-ce4','vivo-v30-5g','apple-iphone-12','motorola-edge-50-pro','realme-12-pro-5g','iqoo-z9-5g']
for i in phone_list:
    overall_rating(df,i)


# In[18]:


overall_ratings_df=pd.DataFrame(overall_ratings_list)


# In[19]:


overall_ratings_df


# In[20]:


overall_ratings_df.to_sql(name='final_scores',con=engine,if_exists='append',index=False)


# In[ ]:




