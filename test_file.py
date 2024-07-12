import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import plotly.express as px

lists = [
    [
        'https://www.flipkart.com/vivo-v30-5g-classic-black-256-gb/p/itme3a94b78a025f?pid=MOBGYGCBHGAK8WGS&lid=LSTMOBGYGCBHGAK8WGSJSYWAR&marketplace=FLIPKART&q=www.flipkart.com%2Fvivo-v30-5g-classic-black-256-gb&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=ca7a7f9f-642d-4502-b7f9-821fa0e4a633.MOBGYGCBHGAK8WGS.SEARCH&ppt=sp&ppn=sp&ssid=rahfrxcwpc0000001720768304441&qH=4883199576b54f18',
        'vivo-v30-5g'],
    [
        'https://www.flipkart.com/samsung-galaxy-s23-fe-purple-128-gb/p/itm03da6b42ff68e?pid=MOBGVTA24G7GHE6M&lid=LSTMOBGVTA24G7GHE6MN4I8LB&marketplace=FLIPKART&q=samsung+galaxy+S23&store=tyy%2F4io&srno=s_1_3&otracker=search&otracker1=search&fm=Search&iid=47fae1d3-eb4a-49df-9367-50e737e79f19.MOBGVTA24G7GHE6M.SEARCH&ppt=sp&ppn=sp&ssid=099wrf380g0000001720768211661&qH=15b83e9c92a1fa60',
        'samsung-galaxy-s23'],
    [
        'https://www.flipkart.com/poco-x3-pro-steel-blue-128-gb/p/itm527548fcdf883?pid=MOBGFKNF6HFYZWPY&lid=LSTMOBGFKNF6HFYZWPYH0RJAD&marketplace=FLIPKART&q=poco+x3+pro&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=551b593c-418c-4fdd-a248-9b0835bb3eda.MOBGFKNF6HFYZWPY.SEARCH&ppt=pp&ppn=pp&ssid=stwaxwtreo0000001720768384633&qH=5fa2a9dbeb17d9d2',
        'poco-x3-pro'],
    [
        'https://www.flipkart.com/apple-iphone-12-blue-64-gb/p/itm5778ad0d0d255?pid=MOBFWBYZ8DNJNY7N&lid=LSTMOBFWBYZ8DNJNY7NMWAWOJ&marketplace=FLIPKART&q=apple+12+&store=tyy%2F4io&srno=s_1_3&otracker=search&otracker1=search&fm=Search&iid=f1ede9b8-2c6c-4a08-ae80-b21c815febe9.MOBFWBYZ8DNJNY7N.SEARCH&ppt=sp&ppn=sp&ssid=9ez5iwjnu80000001720768140721&qH=e28470a0958e0761',
        'apple-iphone-12'],
    [
        'https://www.flipkart.com/oneplus-nord-ce4-celadon-marble-128-gb/p/itm5a09089114afb?pid=MOBGZN8YJ4KZ2KNH&lid=LSTMOBGZN8YJ4KZ2KNHHWWVQA&marketplace=FLIPKART&q=oneplus+nord+ce4&store=tyy%2F4io&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_15_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_15_na_na_ps&fm=Search&iid=6a45a802-b4aa-47b7-8b15-60b41789d4be.MOBGZN8YJ4KZ2KNH.SEARCH&ppt=sp&ppn=sp&ssid=9bzpr15i2o0000001720768440270&qH=be802f2b6dfde2b2',
        'oneplus-nord-ce4'],
    [
        'https://www.flipkart.com/motorola-edge-50-pro-5g-68w-charger-luxe-lavender-256-gb/p/itmba8105d0d22ad?pid=MOBGXFXYMTKAMPTS&lid=LSTMOBGXFXYMTKAMPTSJQVWQM&marketplace=FLIPKART&q=motorola+edge+50+pro&store=tyy%2F4io&spotlightTagId=BestsellerId_tyy%2F4io&srno=s_1_2&otracker=AS_QueryStore_OrganicAutoSuggest_2_11_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_2_11_na_na_ps&fm=search-autosuggest&iid=7a155812-a11d-49d9-b5e0-8499e111b0d5.MOBGXFXYMTKAMPTS.SEARCH&ppt=sp&ppn=sp&ssid=8a2rmo18k00000001720768472372&qH=b3629d8b06502c5a',
        'motorola-edge-50-pro'],
    [
        'https://www.flipkart.com/realme-12-pro-5g-navigator-beige-256-gb/p/itmcc78f150eeabd?pid=MOBGYQ6BVDHRJRSG&lid=LSTMOBGYQ6BVDHRJRSGDKJZZD&marketplace=FLIPKART&q=realme+12+pro+5g&store=tyy%2F4io&srno=s_1_4&otracker=search&otracker1=search&fm=search-autosuggest&iid=00df3227-72b1-4a25-a2da-92d072cec478.MOBGYQ6BVDHRJRSG.SEARCH&ppt=sp&ppn=sp&ssid=lw59w9g6mo0000001720768524533&qH=1e49302487f3a7e6',
        'realme-12-pro-5g'],

    [
        'https://www.flipkart.com/iqoo-z9-5g-brushed-green-256-gb/p/itm4bdb51f6a3f34?pid=MOBGZYZRNM766B5F&lid=LSTMOBGZYZRNM766B5F0M34WL&marketplace=FLIPKART&q=iqoo+neo+z9+5g&store=tyy%2F4io&srno=s_1_9&otracker=search&otracker1=search&fm=search-autosuggest&iid=f4bcba16-4b70-4352-88eb-2f27bc978f32.MOBGZYZRNM766B5F.SEARCH&ppt=sp&ppn=sp&ssid=hstzopbkpc0000001720768640457&qH=054e1bedcd44a88f',
        'iqoo-z9-5g']

]

# Load and set the application icon
icon_path = "C:/Users/akash/PycharmProjects/pythonProject/sentiment_based_product_recommendation/flipkart_image.jpg"
icon = Image.open(icon_path)
st.set_page_config(
    page_title="Sentiment Based Product Recommendation | By Akash S",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This dashboard app is created by Akash
                            It provides product recommendations based on sentiment analysis."""}
)

# Sidebar header
st.sidebar.header("Dashboard")

# Step 1: Load Data from SQL
engine = create_engine('mysql+pymysql://root:2261389@localhost/recommendation')
query = "SELECT * FROM reviews_with_aspect_ratings"
data = pd.read_sql(query, engine)

menu_select = st.sidebar.selectbox("Menu",
                                   ["Home", "Product Recommendation", "Comparison Analysis", "Performance Analysis"])

# Custom CSS for styling
st.markdown("""
    <style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .big-chart {
        width: 100%;
        height: 600px;
    }
    .centered-title {
        text-align: center;
        margin-bottom: 1rem;
    }
    .centered-title h1 {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4B0082;
        margin: 0;
    }
    .centered-title h2 {
        font-size: 1.5rem;
        margin-top: 0.5rem;
    }
    .centered-title h3 {
        font-size: 1.2rem;
        color: violet;
        margin-top: 0.5rem;
    }
    .tech-list {
        list-style-type: none;
        padding: 0;
        text-align: left;
    }
    .tech-list li {
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
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


if menu_select == "Home":
    # Main content for the homepage
    st.markdown("<h1 style='text-align: center;'>Sentiment Based Product Recommendation System</h1>",
                unsafe_allow_html=True)

    # Image and markdown sections
    st.image(
        icon_path,
        width=300
    )

    st.markdown("# :violet[Product Recommendation]")
    st.markdown("## :violet[A User-Friendly Tool Using NLP and streamlit]")

    st.markdown("### :violet[Domain:] **Fintech**")
    st.markdown("### :violet[Technologies Used:]")
    st.markdown("- Selenium")
    st.markdown("- Python, Pandas")
    st.markdown("- Transformers, Scikit-Learn")
    st.markdown("- Sqlalchemy, Streamlit")

    st.markdown("## :rocket: Overview")
    st.markdown(
        " Web scrap Phones from range 20,000 to 40,000 from Flipkart using Selenium and find the sentiment analysis using langchain and make recommendations to the users"
    )

    st.markdown("### :bulb: Key Features")
    st.markdown("- Build a sentiment-based product recommendation system")
    st.markdown("- Analyze top-performing products based on sentiment scores")
    st.markdown("- Interactive bar charts, pie charts for deeper insights")

    # Additional images or sections can be added similarly

    # Ensure everything is displayed
    st.sidebar.markdown("---")  # Separator for sidebar
    st.markdown("---")  # Separator for main content

elif menu_select == "Product Recommendation":
    st.markdown("<h1 style='text-align: center;'>Recommendation Engine</h1>", unsafe_allow_html=True)

    user_prompt = st.text_input('Enter your Query:')
    if user_prompt:
        recommended_product = suggest_product(user_prompt, product_features)
        st.write("Recommended product:", recommended_product)
        for i in lists:
            if i[1] == recommended_product:
                st.markdown(f"[Click here to visit Flipkart]({i[0]})")
# Additional sections for other menu options can be added here
elif menu_select == "Comparison Analysis":
    def visualization(feature, Price):

        sub_df = pd.read_sql(
            f'select name,round({feature},2) as score from merged_df where Price<={Price} order by score desc',
            engine)

        # Create pie chart
        fig = px.pie(sub_df, names='name', values='score')

        # Display the pie chart in Streamlit
        feature = f"{feature}"  # Replace this with your dynamic feature variable
        st.markdown(
            f"<h3 style='text-align: center; font-weight: bold;'>Distribution for All Phones based on {feature}</h3>",
            unsafe_allow_html=True)

        st.plotly_chart(fig)


    st.markdown("<h1 style='text-align: center;'>Comparison Analysis</h1>", unsafe_allow_html=True)

    df = pd.read_sql('select * from final_scores', engine)
    feature_list = df.columns.tolist()
    feature_select = st.sidebar.selectbox('Select the features to be compared', options=feature_list[1:])
    price = st.sidebar.slider('select price values', 20000, 40000, 40000,5000)

    visualization(feature_select, price)


elif menu_select == "Performance Analysis":
    def performance_visualization(phone_name):
        sub_df = pd.read_sql(f"select * from final_scores where name='{phone_name}'", engine)
        df_rounded = sub_df.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)
        st.table(df_rounded)


    st.markdown("<h1 style='text-align: center;'>Phone Performance Analysis</h1>", unsafe_allow_html=True)
    df = pd.read_sql('select name from final_scores', engine)
    names = df.name.tolist()
    select_phone = st.sidebar.selectbox('Select the phone', options=names)
    performance_visualization(select_phone)

else:
    pass
