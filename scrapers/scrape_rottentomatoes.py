"""
Rotten Tomatoes movie data provider.

**IMPORTANT NOTE:**
Rotten Tomatoes does NOT have a publicly available API for general use.
Furthermore, their website has strict terms of service that prohibit unauthorized
web scraping.

For these reasons, this script **DOES NOT** scrape or contact Rotten Tomatoes'
servers in any way.

Instead, it provides a hardcoded, sample dataset for educational and
demonstration purposes only. This allows the project to function with
representative data without violating any terms of service.
"""

import json
import os
from typing import List, Dict
from scraper_utils import ScraperUtils, create_movie_document


class RottenTomatoesScraper:
    """Scraper for Rotten Tomatoes movie data."""
    
    BASE_URL = "https://www.rottentomatoes.com"
    
    def __init__(self, output_file: str = "../data/raw/rottentomatoes_movies.json"):
        self.output_file = output_file
        self.movies = []
        self.utils = ScraperUtils()
    
    def scrape_popular_movies(self, limit: int = 50):
        """
        Scrape popular movies from Rotten Tomatoes.
        
        Args:
            limit: Number of movies to scrape
        """
        print("Rotten Tomatoes Scraper")
        print("=" * 60)
        print("NOTE: This is sample data for educational purposes.")
        print("Always respect website terms of service.")
        print()
        
        # Create sample data (replace with actual API or approved scraping)
        self.movies = self._create_sample_data(limit)
        
        print(f"Collected {len(self.movies)} movies from Rotten Tomatoes")
    
    def _create_sample_data(self, count: int) -> List[Dict]:
        """
        Create sample movie data for demonstration.
        """
        sample_movies = [
            {
                "title": "The Godfather",
                "year": 1972,
                "tomatometer": 97,
                "audience_score": 98,
                "genres": ["Crime", "Drama"],
                "directors": ["Francis Ford Coppola"],
                "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
                "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "critic_consensus": "One of Hollywood's greatest critical and commercial successes, The Godfather gets everything right; not only did the movie transcend expectations, it established new benchmarks for American cinema.",
                "num_reviews": 117
            },
            {
                "title": "Pulp Fiction",
                "year": 1994,
                "tomatometer": 92,
                "audience_score": 96,
                "genres": ["Crime", "Drama"],
                "directors": ["Quentin Tarantino"],
                "cast": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
                "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
                "critic_consensus": "One of the most influential films of the 1990s, Pulp Fiction is a delirious post-modern mix of neo-noir thrills, pitch-black humor, and pop-culture touchstones.",
                "num_reviews": 94
            },
            {
                "title": "Mad Max: Fury Road",
                "year": 2015,
                "tomatometer": 97,
                "audience_score": 86,
                "genres": ["Action", "Adventure", "Sci-Fi"],
                "directors": ["George Miller"],
                "cast": ["Tom Hardy", "Charlize Theron", "Nicholas Hoult"],
                "plot": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners and a drifter named Max.",
                "critic_consensus": "Overwhelmingly intense and visually stunning, Mad Max: Fury Road is a kinetic triumph that balances adrenaline and artistry.",
                "num_reviews": 365
            },
            {
                "title": "Everything Everywhere All at Once",
                "year": 2022,
                "tomatometer": 95,
                "audience_score": 90,
                "genres": ["Action", "Adventure", "Sci-Fi"],
                "directors": ["Daniel Kwan", "Daniel Scheinert"],
                "cast": ["Michelle Yeoh", "Stephanie Hsu", "Ke Huy Quan"],
                "plot": "An aging Chinese immigrant is swept up in an insane adventure, where she alone can save the world by exploring other universes connecting with the lives she could have led.",
                "critic_consensus": "Led by an outstanding Michelle Yeoh, Everything Everywhere All at Once is a hilarious and heartrending journey through the multiverse.",
                "num_reviews": 428
            },
            {
                "title": "Get Out",
                "year": 2017,
                "tomatometer": 98,
                "audience_score": 86,
                "genres": ["Horror", "Mystery", "Thriller"],
                "directors": ["Jordan Peele"],
                "cast": ["Daniel Kaluuya", "Allison Williams", "Bradley Whitford"],
                "plot": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point.",
                "critic_consensus": "Funny, scary, and thought-provoking, Get Out seamlessly weaves its trenchant social critiques into a brilliantly effective and entertaining horror/comedy thriller.",
                "num_reviews": 456
            }
        ]
        
        movies = []
        for i in range(min(count, len(sample_movies) * 10)):
            movie_template = sample_movies[i % len(sample_movies)].copy()
            movies.append(movie_template)
        
        return movies[:count]
    
    def save_data(self):
        """Save scraped data to JSON file."""
        documents = []
        
        for movie in self.movies:
            # Average tomatometer and audience score, normalize to 0-10
            avg_score = (movie.get('tomatometer', 0) + movie.get('audience_score', 0)) / 2
            normalized_rating = self.utils.normalize_rating(avg_score, 100)
            
            # Use critic consensus as review text
            reviews = movie.get('critic_consensus', '')
            
            doc = create_movie_document(
                title=movie['title'],
                year=movie['year'],
                site='rottentomatoes',
                url=f"{self.BASE_URL}/m/{movie['title'].lower().replace(' ', '_')}",
                rating=normalized_rating,
                genres=movie.get('genres', []),
                directors=movie.get('directors', []),
                cast=movie.get('cast', []),
                plot=movie.get('plot', ''),
                reviews=reviews,
                num_reviews=movie.get('num_reviews')
            )
            documents.append(doc)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Save to file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(documents)} movies to {self.output_file}")


def main():
    """Main execution function."""
    scraper = RottenTomatoesScraper()
    
    print("Starting Rotten Tomatoes scraper...")
    print()
    
    # Scrape movies
    scraper.scrape_popular_movies(limit=50)
    
    # Save to file
    scraper.save_data()
    
    print("\nRotten Tomatoes scraping complete!")


if __name__ == "__main__":
    main()
