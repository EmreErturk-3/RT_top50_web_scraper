

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Scraper:
    def __init__(self):
        self.base_url = 'https://editorial.rottentomatoes.com/guide/best-movies-of-all-time/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_page(self, url):
        "Get the HTML content of a page"
        delay= random.uniform(1,3)
        print(f"Waiting for {delay} seconds")
        logger.info(f"Waiting for {delay} seconds")
        time.sleep(delay)

        try:
            response = requests.get(url, headers=self.headers,timeout=15)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            error_msg = f"Request Exception: {url}:{e}"
            print(error_msg)
            logger.error(error_msg)
            return None

    def scrape_top_movies(self):
        """Scrape top 50 movies from Rotten Tomatoes"""
        start_msg = "Starting to scrape top 50 Rotten Tomatoes movies"
        print(start_msg)
        logger.info(start_msg)

        html = self.get_page(self.base_url)

        if not html:
            error_msg = "Failed to fetch page"
            print(error_msg)
            logger.error(error_msg)
            return pd.DataFrame()

        soup = BeautifulSoup(html, 'html.parser')
        movies_data = []

        # Find all movie elements
        movie_elements = soup.select('div.row.countdown-item')

        if not movie_elements:
            error_msg = "No movie elements found. "
            print(error_msg)
            logger.error(error_msg)
            return pd.DataFrame()

        print(f"Found {len(movie_elements)} movie elements")
        logger.info(f"Found {len(movie_elements)} movie elements")

        #Process movie elements
        for idx, element in enumerate(movie_elements):
            try:
                #Extract rank
                rank_elem= element.select_one('div.countdown-index')
                rank =idx+1
                if rank_elem:
                    rank_text = rank_elem.text.strip()
                    rank_match = re.search(r'#?(\d+)', rank_text)
                    if rank_match:
                        rank = int(rank_match.group(1))

                # Extract title
                title_elem =element.select_one('h2')
                title= 'Unknown'
                score_in_title= "Unknown"

                if title_elem:
                    full_text = title_elem.text.strip()
                    score_match = re.search(r'(\d+%)', full_text)
                    if score_match:
                        score_in_title = score_match.group(1)
                        full_text = full_text.replace(score_match.group(1), '').strip()

                    title = re.sub(r'^#?\d+[.:]\s*', '', full_text)

                #Extract score
                score_elem = element.select_one('span.tMeterScore')
                score_from_elem= "Unknown"
                if score_elem:
                    score_from_elem = score_elem.text.strip()

                score= score_from_elem if score_from_elem != "Unknown" else score_in_title

                # Extract year
                year = "Unknown"
                year_match = re.search(r'\((\d{4})\)', title)

                if year_match:
                    year = year_match.group(1)
                    title=  re.sub(r'\s*\(\d{4}\)\s*', '', title).strip()

                title = re.sub(r'\s+', ' ', title).strip()

                movies_data.append({
                    'rank': rank,
                    'title': title,
                    'year': year,
                    'score': score,
                })

                movie_msg = f"Scraped #{rank}: {title} ({year})- Score: ({score})"
                print(movie_msg)
                logger.info(movie_msg)

            except Exception as e:
                error_msg: f"Error parsing movie {idx+1}:{e}"
                print(error_msg)
                logger.error(error_msg)
                continue
        # Create DataFrame and sort by rank
        df = pd.DataFrame(movies_data)
        if not df.empty and 'rank 'in df.columns:
            df = df.sort_values('rank').reset_index(drop=True)

        #Save to CSV
        filename = 'rt_top50_movies.csv'
        df.to_csv(filename, index=False)
        saved_msg = f"Saved to {filename}"
        print(saved_msg)
        logger.info(saved_msg)
        return df

if __name__ == "__main__":
    scraper=Scraper()
    movies_df = scraper.scrape_top_movies()

    if not movies_df.empty:
        print("Scraped top 50 movies")
        print(movies_df.head(15))