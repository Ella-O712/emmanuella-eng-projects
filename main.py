import logging

import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    filename='web_scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def scrape_techcrunch_headlines():
    """
    Scrapes the latest headlines from the TechCrunch homepage.
    """
    url = 'https://techcrunch.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'}
    logging.info("Starting web scraping")

    try:

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            headlines = soup.find_all('h2')
            headline_texts = [headline.get_text().strip() for headline in headlines]

            if not headline_texts:
                print("No headlines found. Check the HTML structure or tag used.")
                logging.warning("No headlines found in the scraped content.")
                return None

            headline_df = pd.DataFrame(headline_texts, columns=['Headline'])

            headline_df['Word_Count'] = headline_df['Headline'].apply(lambda x: len(x.split()))
            headline_df['Character_Count'] = headline_df['Headline'].apply(lambda x: len(x))

            headline_df.to_csv('techcrunch_headlines.csv', index=False)
            logging.info("Successfully scraped and saved headlines to techcrunch_headlines.csv")

            print(headline_df.head())

            return headline_df

        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during web scraping: {e}")
        print(f"Failed to retrieve the webpage: {e}")
        return None


def visualize_data(dataframe):
    """
    Visualizes the distribution of word counts and character counts in the headlines.
    """
    try:

        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        dataframe['Word_Count'].plot(kind='hist', bins=10, color='white', edgecolor='black')
        plt.title('Distribution of Headline Word Count')
        plt.xlabel('Word Count')
        plt.ylabel('Frequency')

        plt.subplot(1, 2, 2)
        dataframe['Character_Count'].plot(kind='hist', bins=10, color='salmon', edgecolor='black')
        plt.title('Distribution of Headline Character Count')
        plt.xlabel('Character Count')
        plt.ylabel('Frequency')

        plt.tight_layout()
        plt.savefig('headline_distributions.png')
        plt.show()
        logging.info("Data visualization completed and saved to headline_distributions.png")

    except Exception as e:
        logging.error(f"Error during visualization: {e}")
        print(f"Failed to visualize data: {e}")


if __name__ == "__main__":

    headline_data = scrape_techcrunch_headlines()

    if headline_data is not None:
        visualize_data(headline_data)
