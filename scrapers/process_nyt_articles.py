"""
Fetches movie-related articles from the New York Times Article Search API.

This script reads movie titles and years from the processed IMDb data,
then queries the NYT API to find relevant movie reviews or articles.

**Setup:**
1. Get a free NYT API key at: https://developer.nytimes.com/get-started
2. Create a file named `.env` in the `scrapers/` directory.
3. Add your API key to the `.env` file like this:
   NYT_API_KEY="YOUR_API_KEY"
"""

import requests
import json
import os
import time
from dotenv import load_dotenv
from typing import List, Dict, Optional, Tuple
from tqdm import tqdm

# --- Configuration ---
API_BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
IMDB_INPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'imdb_movies.json')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'nyt_articles.json')

# Load API credentials from .env file
load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

class NYTArticleProcessor:
    """Fetches movie review articles from the NYT API."""

    def __init__(self, input_file: str = IMDB_INPUT_FILE, output_file: str = OUTPUT_FILE):
        self.input_file = input_file
        self.output_file = output_file
        self.articles: List[Dict] = []

    def _get_movies_to_process(self) -> List[Tuple[str, str, int]]:
        """Loads IMDb ID, title, and year from the IMDb JSON file."""
        if not os.path.exists(self.input_file):
            print(f"ERROR: IMDb input file not found at {self.input_file}")
            print("Please run the process_imdb_data.py script first.")
            return []
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            imdb_data = json.load(f)
        
        movies = [
            (movie.get('tconst'), movie.get('title'), movie.get('year'))
            for movie in imdb_data
            if movie.get('tconst') and movie.get('title') and movie.get('year')
        ]
        print(f"Loaded {len(movies)} movies to search for in NYT.")
        return movies

    def fetch_articles_for_movie(self, title: str, year: int) -> List[Dict]:
        """Fetches articles for a single movie from the NYT API."""
        if not API_KEY:
            return []

        # Construct a query that is likely to find a movie review
        query = f'"{title}"'
        # Filter query to the year of release and the year after
        filter_query = f'pub_year:({year} OR {year + 1}) AND type_of_material:("Review")'
        
        params = {
            "q": query,
            "fq": filter_query,
            "api-key": API_KEY,
            "sort": "relevance"
        }
        try:
            response = requests.get(API_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("response", {}).get("docs", [])
        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 401:
                raise ValueError("NYT API key is invalid (401 Unauthorized). Halting NYT processing.")
            elif e.response and e.response.status_code == 429:
                print(f"Rate limit hit for '{title}'. Pausing for 60 seconds...")
                time.sleep(60)
                return self.fetch_articles_for_movie(title, year) # Retry after pause
            
            print(f"Error fetching articles for '{title}': {e}")
            return []

    def process_movies(self, limit: int = 0):
        """
        Iterates through movies, fetches articles from NYT, and saves them.
        """
        if not API_KEY:
            print("ERROR: NYT_API_KEY not found.")
            print("Please create a .env file in the scrapers/ directory with your key.")
            return

        movies_to_process = self._get_movies_to_process()
        if not movies_to_process:
            return

        if limit > 0:
            movies_to_process = movies_to_process[:limit]
            print(f"Processing a limit of {limit} movies.")

        for imdb_id, title, year in tqdm(movies_to_process, desc="Fetching from NYT"):
            articles = self.fetch_articles_for_movie(title, year)
            if articles:
                # Usually, the most relevant article is the first one
                for article in articles[:2]: # Take top 2 most relevant
                    formatted_article = self._format_document(article, imdb_id, title)
                    self.articles.append(formatted_article)
            
            # NYT API has a rate limit of ~10 requests/minute. Sleep for 7 seconds for safety.
            time.sleep(7)

    def _format_document(self, article: Dict, imdb_id: str, movie_title: str) -> Dict:
        """Formats the NYT API response into our document structure."""
        return {
            "id": f"nyt_{article.get('_id')}",
            "imdb_id": imdb_id,
            "movie_title": movie_title,
            "headline": article.get("headline", {}).get("main"),
            "abstract": article.get("abstract"),
            "snippet": article.get("snippet"),
            "lead_paragraph": article.get("lead_paragraph"),
            "pub_date": article.get("pub_date"),
            "web_url": article.get("web_url"),
            "source": "The New York Times"
        }

    def save_data(self):
        """Saves the processed articles to a JSON file."""
        if not self.articles:
            print("No articles to save.")
            return

        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.articles)} articles to {self.output_file}")


def main():
    """Main execution function."""
    print("Starting NYT article processing...")

    if os.path.exists(OUTPUT_FILE):
        print(f"NYT data already exists at {OUTPUT_FILE}. Skipping.")
        return

    processor = NYTArticleProcessor()
    # Process a small subset for demonstration to avoid long waits
    processor.process_movies(limit=10) 
    processor.save_data()
    print("\nNYT processing complete!")


if __name__ == "__main__":
    main()
