from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine
import pandas as pd
import time
# import tensorflow as tf

# Database connection
engine = create_engine('mysql+pymysql://root:2261389@localhost/recommendation')

# Links to scrape
lists = [[
             'https://www.flipkart.com/vivo-v30-5g-classic-black-256-gb/product-reviews/itme3a94b78a025f?pid=MOBGYGCBHGAK8WGS&lid=LSTMOBGYGCBHGAK8WGSJSYWAR&marketplace=FLIPKART',
             'vivo-v30-5g'],
         [
             'https://www.flipkart.com/samsung-galaxy-s23-fe-purple-128-gb/product-reviews/itm03da6b42ff68e?pid=MOBGVTA24G7GHE6M&lid=LSTMOBGVTA24G7GHE6MN4I8LB&marketplace=FLIPKART',
             'samsung-galaxy-s23'],
         [
             'https://www.flipkart.com/poco-x3-pro-graphite-black-128-gb/product-reviews/itm9ce5166bf0e03?pid=MOBGFKNFRVPZ77GX&lid=LSTMOBGFKNFRVPZ77GXPOKQYD&marketplace=FLIPKART',
             'poco-x3-pro'],
         [
             'https://www.flipkart.com/iqoo-neo-7-pro-fearless-flame-128-gb/product-reviews/itm1585345e64a32?pid=MOBGRHFZFJPGSQ9H&lid=LSTMOBGRHFZFJPGSQ9HQRZRLU&marketplace=FLIPKART',
             'iqoo-neo-7-pro'],
         [
             'https://www.flipkart.com/oneplus-nord-ce4-celadon-marble-256-gb/product-reviews/itm5a09089114afb?pid=MOBGZZGY8FRH5Y7R&lid=LSTMOBGZZGY8FRH5Y7RE7OAXA&marketplace=FLIPKART',
             'oneplus-nord-ce4'],

         ]



def scrape_reviews(browser):
    try:
        # Find review elements using the updated XPath
        review_elements = browser.find_elements(By.XPATH, "//div[contains(@class, 'ZmyHeo')]")
        # Extract the text from each review element
        reviews = [element.text for element in review_elements if element.text.strip()]
        return reviews
    except Exception as e:
        print(f"Exception occurred while scraping reviews: {e}")
        return []


def scrape_products(base_url, name):
    df = pd.DataFrame(columns=['Name', 'Review'])
    browser = webdriver.Chrome()
    try:
        # Open the webpage
        browser.get(base_url)

        all_reviews = []
        count = 10

        while True:
            try:
                if count >= 12:
                    pass
                else:
                    count += 1

                # Scrape reviews from the current page
                reviews = scrape_reviews(browser)

                if not reviews:
                    print("No reviews found on the current page.")
                    break

                all_reviews.extend(reviews)

                # Find and click the "Next" button
                next_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
                    (By.XPATH,
                     f'''//*[@id="container"]/div/div[3]/div/div/div[2]/div[13]/div/div/nav/a[{count}]/span''')))
                next_button.click()

                # Wait for the next page to load
                time.sleep(2)  # Adjust the sleep time as necessary
            except Exception as e:
                print(f"Exception occurred while clicking 'Next' button or scraping reviews: {e}")
                break

    except Exception as e:
        print(f"Exception occurred: {e}")

    finally:
        # Close the browser
        browser.quit()

        # Prepare DataFrame
        df = pd.DataFrame({'Name': [name] * len(all_reviews), 'Reviews': all_reviews})

        df.to_sql(name='sentiment_reviews', con=engine, if_exists='append', index=False)
        print(f'The records of length {len(all_reviews)} for the {name} are uploaded to SQL.')


for i in lists:
    scrape_products(i[0], i[1])
