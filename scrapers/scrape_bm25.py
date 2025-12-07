"""
BM25-based movie search provider.

This module does NOT scrape or contact any external servers.
Instead, it uses sample movie data for demonstration and testing purposes.
"""

import json
import os
from typing import List, Dict
from rank_bm25 import BM25Okapi
from scraper_utils import create_movie_document


class BM25MovieProvider:
    """Simple BM25 search provider using sample movie data."""

    def __init__(self, output_file: str = "../data/raw/bm25_movies.json"):
        self.output_file = output_file
        self.movies = []
        self.documents = []
        self.bm25 = None

    def load_sample_movies(self):
        """Load sample movies for BM25 indexing."""
        print("BM25 Sample Movie Provider")
        print("=" * 60)
        print("Using local sample dataset for demonstration.")
        print()

        self.movies = self._create_sample_data()
        print(f"Loaded {len(self.movies)} sample movies.")

    def _create_sample_data(self) -> List[Dict]:
        """Hardcoded sample data to mimic a scraped dataset."""
        return [
            {
                "title": "Inception",
                "year": 2010,
                "genres": ["Action", "Sci-Fi"],
                "directors": ["Christopher Nolan"],
                "cast": ["Leonardo DiCaprio", "Elliot Page", "Tom Hardy"],
                "plot": "A thief who steals corporate secrets through dream-sharing technology is tasked with planting an idea into a CEO's mind.",
                "reviews": "A mind-bending sci-fi masterpiece blending dreams and reality.",
                "rating": 8.7,
                "num_reviews": 2100,
            },
            {
                "title": "The Matrix",
                "year": 1999,
                "genres": ["Action", "Sci-Fi"],
                "directors": ["Lana Wachowski", "Lilly Wachowski"],
                "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
                "plot": "A hacker discovers that his reality is a simulation controlled by intelligent machines.",
                "reviews": "Innovative visuals and groundbreaking cyberpunk storytelling.",
                "rating": 8.6,
                "num_reviews": 1900,
            },
            {
                "title": "The Shawshank Redemption",
                "year": 1994,
                "genres": ["Drama"],
                "directors": ["Frank Darabont"],
                "cast": ["Tim Robbins", "Morgan Freeman"],
                "plot": "Two imprisoned men forge a deep friendship and find hope through acts of kindness.",
                "reviews": "An inspiring story of hope, resilience, and human dignity.",
                "rating": 9.3,
                "num_reviews": 2500,
            }
        ]

    def build_index(self):
        """Build BM25 index from movie metadata."""
        print("Building BM25 index...")

        corpus = []
        self.documents = []

        for movie in self.movies:
            text = " ".join([
                movie.get("title", ""),
                movie.get("plot", ""),
                " ".join(movie.get("genres", [])),
                " ".join(movie.get("directors", [])),
                " ".join(movie.get("cast", [])),
                movie.get("reviews", ""),
            ]).lower()

            corpus.append(text.split())
            self.documents.append(text)

        self.bm25 = BM25Okapi(corpus)
        print("BM25 index built successfully.")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search movies using BM25 ranking."""
        if not self.bm25:
            raise ValueError("Index not built. Call build_index() first.")

        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            zip(self.movies, scores), key=lambda x: x[1], reverse=True
        )

        return [m for m, _ in ranked[:top_k]]

    def save_data(self):
        """Save processed movie dataset to JSON file."""
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

        docs = []
        for movie in self.movies:
            doc = create_movie_document(
                title=movie["title"],
                year=movie["year"],
                site="bm25",
                url=f"bm25://{movie['title'].lower().replace(' ', '_')}",
                rating=movie.get("rating", 0),
                genres=movie.get("genres", []),
                directors=movie.get("directors", []),
                cast=movie.get("cast", []),
                plot=movie.get("plot", ""),
                reviews=movie.get("reviews", ""),
                num_reviews=movie.get("num_reviews", 0),
            )
            docs.append(doc)

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(docs, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(docs)} movie documents to {self.output_file}")


def main():
    provider = BM25MovieProvider()
    provider.load_sample_movies()
    provider.build_index()
    provider.save_data()
    print("BM25 provider ready.")


if __name__ == "__main__":
    main()
