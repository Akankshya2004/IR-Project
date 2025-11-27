# Movie Information Retrieval System

## Project Overview

This is a university Information Retrieval course project that implements an end-to-end movie search system using Apache Solr.

### Team Members
- Student 1
- Student 2

### Project Goals
- Scrape movie data from at least 3 different websites
- Index data in Apache Solr
- Build a web interface with search capabilities
- Implement one simple IR feature (faceted search)
- Implement one advanced IR feature (More Like This)
- Conduct user evaluation

## Project Structure

```
Project/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config/
│   ├── managed-schema        # Solr schema configuration
│   └── solr-setup.md         # Solr installation and setup instructions
├── scrapers/
│   ├── scrape_imdb.py        # IMDb scraper
│   ├── scrape_rottentomatoes.py  # Rotten Tomatoes scraper
│   ├── scrape_letterboxd.py  # Letterboxd scraper
│   ├── scraper_utils.py      # Common scraping utilities
│   └── merge_data.py         # Merge scraped data into single JSON
├── data/
│   ├── raw/                  # Raw scraped data (one file per site)
│   └── movies.json           # Merged data ready for Solr
├── web/
│   ├── app.py                # Flask application
│   ├── solr_client.py        # Solr query interface
│   ├── templates/
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Home page with search form
│   │   ├── results.html      # Search results page
│   │   └── similar.html      # Similar movies page
│   └── static/
│       ├── css/
│       │   └── style.css     # Stylesheet
│       └── js/
│           └── main.js       # Frontend JavaScript
├── evaluation/
│   ├── evaluation_plan.md    # User evaluation design
│   └── tasks.md              # Evaluation tasks
└── reports/
    └── interim_report.md     # Interim progress report
```

## Tech Stack

- **Search Engine**: Apache Solr 9.x
- **Backend**: Python 3.8+ with Flask
- **Scraping**: requests, beautifulsoup4, lxml
- **Frontend**: HTML5, CSS3, minimal JavaScript
- **Version Control**: Git

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install and Configure Solr

See `config/solr-setup.md` for detailed instructions.

Quick start:
```bash
# Download Solr 9.x
# Start Solr
bin/solr start

# Create movies collection
bin/solr create -c movies

# Apply schema (copy managed-schema or use Schema API)
```

### 3. Scrape Movie Data

```bash
cd scrapers
python scrape_imdb.py
python scrape_rottentomatoes.py
python scrape_letterboxd.py
python merge_data.py
```

This will create `data/movies.json` with merged data.

### 4. Index Data in Solr

```bash
cd <solr-installation>
bin/post -c movies ../Project/data/movies.json
```

### 5. Run Web Application

```bash
cd web
python app.py
```

Open browser to `http://localhost:5000`

## Features

### Basic Search
- Single search box querying title, plot, and review text
- Results display with title, year, rating, genres, and snippet
- Pagination (10 results per page)
- Links to original movie pages

### Simple IR Feature: Faceted Search
- Filter by genre (Action, Comedy, Drama, etc.)
- Filter by year range (2000-2024)
- Filter by rating (e.g., > 7.0)
- Multiple facets can be applied simultaneously

### Advanced IR Feature: More Like This
- "Find Similar Movies" button on each result
- Uses Solr MoreLikeThis to find similar movies based on:
  - Plot text similarity
  - Genre overlap
  - Cast and director overlap
- Shows top 5 similar movies with similarity scores

## Evaluation Plan

User evaluation will compare:
- Baseline interface (basic search only)
- Full interface (with faceted search and More Like This)

Metrics:
- Task completion success rate
- Time to complete tasks
- Number of queries needed
- User satisfaction ratings (1-5 scale)

See `evaluation/evaluation_plan.md` for full details.

## Development Timeline

- Week 1-2: Data scraping and cleaning
- Week 3: Solr setup and indexing
- Week 4: Basic web interface
- Week 5: Simple and advanced features
- Week 6: User evaluation
- Week 7-8: Final report

## License

Academic project - not for commercial use.
