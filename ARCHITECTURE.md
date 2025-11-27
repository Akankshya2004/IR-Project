# System Architecture

This document provides visual representations of the Movie IR System architecture.

## High-Level System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                    (Web Browser - HTML/CSS/JS)                   │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Search Box  │  │   Facets     │  │   Results    │          │
│  │              │  │  (Filters)   │  │    List      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │ More Like    │  │  Pagination  │                             │
│  │    This      │  │              │                             │
│  └──────────────┘  └──────────────┘                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP Requests
                           │ (GET /search, /similar)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK APPLICATION                           │
│                        (Python Backend)                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Route Handlers                         │   │
│  │  • / (home)                                              │   │
│  │  • /search (query processing)                            │   │
│  │  • /similar/<id> (recommendations)                       │   │
│  │  • /api/stats, /api/autocomplete                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  Solr Client Layer                        │   │
│  │  • Query building                                        │   │
│  │  • Filter construction                                   │   │
│  │  • Result parsing                                        │   │
│  │  • Facet extraction                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/JSON
                           │ (Solr Query API)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       APACHE SOLR                                │
│                   (Search Engine Backend)                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  'movies' Collection                      │   │
│  │                                                           │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │              Inverted Index                        │  │   │
│  │  │  • text → [doc1, doc2, ...]                       │  │   │
│  │  │  • genres → [doc3, doc5, ...]                     │  │   │
│  │  │  • year → [2010: doc1, 2015: doc2, ...]          │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │            Query Processing                        │  │   │
│  │  │  • Tokenization & Analysis                        │  │   │
│  │  │  • TF-IDF / BM25 Ranking                          │  │   │
│  │  │  • Facet Computation                              │  │   │
│  │  │  • MoreLikeThis (MLT)                             │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │              Document Store                        │  │   │
│  │  │  {id, title, year, genres, plot, ...}             │  │   │
│  │  │  {id, title, year, genres, plot, ...}             │  │   │
│  │  │  ...                                               │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Indexed from
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      DATA PIPELINE                               │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   IMDb       │  │  Rotten      │  │ Letterboxd   │          │
│  │  Scraper     │  │ Tomatoes     │  │   Scraper    │          │
│  │              │  │  Scraper     │  │              │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
│         ▼                  ▼                  ▼                  │
│  ┌──────────────────────────────────────────────────┐           │
│  │            Data Merger & Deduplication            │           │
│  │  • Group by (title, year)                        │           │
│  │  • Merge duplicates                              │           │
│  │  • Normalize ratings                             │           │
│  │  • Combine metadata                              │           │
│  └──────────────────────────────────────────────────┘           │
│                           │                                       │
│                           ▼                                       │
│                    movies.json                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow: Search Query

```
1. User enters query "action thriller 2020"
   │
   ▼
2. Browser sends GET /search?q=action+thriller+2020&genres=Action
   │
   ▼
3. Flask route handler processes request
   │
   ├─ Extract query: "action thriller 2020"
   ├─ Extract filters: genres=["Action"]
   └─ Extract pagination: page=1
   │
   ▼
4. Solr client builds query
   │
   ├─ Main query: text:"action thriller 2020"
   ├─ Filter query: genres:"Action"
   ├─ Facets: genres, year
   ├─ Highlight: plot, reviews
   └─ Pagination: start=0, rows=10
   │
   ▼
5. Send HTTP request to Solr
   │
   GET http://localhost:8983/solr/movies/select?
       q=text:action+thriller+2020
       &fq=genres:"Action"
       &facet=true
       &facet.field=genres
       &facet.field=year
       &hl=true
       &hl.fl=plot,reviews
       &start=0
       &rows=10
   │
   ▼
6. Solr processes query
   │
   ├─ Tokenize: [action, thriller, 2020]
   ├─ Search index for matching documents
   ├─ Score documents (TF-IDF/BM25)
   ├─ Apply filters (genres=Action)
   ├─ Compute facets (count by genre, year)
   ├─ Generate highlights
   └─ Sort by relevance
   │
   ▼
7. Solr returns JSON response
   │
   {
     "response": {
       "numFound": 42,
       "docs": [
         {id, title, year, rating, genres, plot, ...},
         ...
       ]
     },
     "facet_counts": {
       "facet_fields": {
         "genres": ["Action", 42, "Thriller", 38, ...],
         "year": [2020, 15, 2019, 12, ...]
       }
     },
     "highlighting": {
       "doc_id": {
         "plot": ["...highlighted text..."]
       }
     }
   }
   │
   ▼
8. Solr client parses response
   │
   ├─ Extract documents
   ├─ Parse facets into list format
   ├─ Map highlighting to documents
   └─ Return structured dict
   │
   ▼
9. Flask renders results.html template
   │
   ├─ Pass documents to template
   ├─ Pass facets for sidebar
   ├─ Pass pagination info
   └─ Apply highlighting
   │
   ▼
10. Return HTML to browser
    │
    ▼
11. User sees results with highlights and facets
```

## Data Flow: More Like This

```
1. User clicks "Find Similar Movies" on "The Dark Knight"
   │
   ▼
2. Browser sends GET /similar/imdb_abc123
   │
   ▼
3. Flask route handler
   │
   ├─ Extract doc_id: "imdb_abc123"
   └─ Call solr_client.more_like_this(doc_id)
   │
   ▼
4. Solr client builds MLT query
   │
   ├─ Main query: id:imdb_abc123
   ├─ MLT enabled: true
   ├─ MLT fields: text, genres, cast, directors
   ├─ MLT parameters: mindf=1, mintf=1, maxqt=25
   └─ Rows: 10
   │
   ▼
5. Send to Solr MLT handler
   │
   GET http://localhost:8983/solr/movies/mlt?
       q=id:imdb_abc123
       &mlt=true
       &mlt.fl=text,genres,cast,directors
       &mlt.mindf=1
       &mlt.mintf=1
       &rows=10
   │
   ▼
6. Solr MLT processing
   │
   ├─ Retrieve source document (The Dark Knight)
   ├─ Extract significant terms from MLT fields
   │  • plot: [batman, joker, gotham, crime, ...]
   │  • genres: [Action, Crime, Drama]
   │  • cast: [Christian Bale, Heath Ledger, ...]
   ├─ Build "like this" query from terms
   ├─ Search for documents matching those terms
   ├─ Rank by similarity (cosine/TF-IDF)
   └─ Return top N most similar
   │
   ▼
7. Solr returns similar documents
   │
   [
     {id, title: "Batman Begins", year: 2005, ...},
     {id, title: "Joker", year: 2019, ...},
     {id, title: "Heat", year: 1995, ...},
     ...
   ]
   │
   ▼
8. Flask renders similar.html template
   │
   ├─ Show source movie (The Dark Knight)
   └─ List similar movies
   │
   ▼
9. User sees similar movies
```

## Faceted Search Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SIDEBAR FACETS                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Genres                                            │     │
│  │  ☑ Action (42)                                     │     │
│  │  ☐ Comedy (28)                                     │     │
│  │  ☐ Drama (56)                                      │     │
│  │  ☑ Thriller (38)                                   │     │
│  │  ...                                               │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Year Range                                        │     │
│  │  Min: [2000  ]  Max: [2024  ]                     │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Minimum Rating                                    │     │
│  │  [Any rating ▼]                                    │     │
│  │    7.0+                                            │     │
│  │    8.0+                                            │     │
│  │    9.0+                                            │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  [Apply Filters]  [Clear All]                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ On change/submit
                           ▼
              Build Solr filter queries (fq):
              • fq=genres:"Action"
              • fq=genres:"Thriller"  
              • fq=year:[2000 TO 2024]
              • fq=rating:[7.0 TO *]
                           │
                           ▼
                    Execute Solr query
                           │
                           ▼
              Results filtered by all facets
              Facet counts updated dynamically
```

## Schema Design

```
┌─────────────────────────────────────────────────────────────┐
│                      Solr Document                           │
│                                                              │
│  id: "imdb_abc123def456"                                    │
│  title: "Inception"              [text_title, indexed]      │
│  year: 2010                      [pint, indexed]            │
│  rating: 8.8                     [pfloat, indexed]          │
│  genres: ["Action", "Sci-Fi"]    [string, multiValued]      │
│  directors: ["C. Nolan"]         [string, multiValued]      │
│  cast: ["DiCaprio", ...]         [string, multiValued]      │
│  plot: "A thief who..."          [text_general, indexed]    │
│  reviews: "Mind-bending..."      [text_general, indexed]    │
│  url: "https://imdb.com/..."     [string, stored only]      │
│  site: "imdb"                    [string, indexed]          │
│  num_reviews: 2543               [pint, indexed]            │
│                                                              │
│  text: [COMBINED COPY FIELD]     [text_general, not stored] │
│    ← title                                                   │
│    ← plot                                                    │
│    ← reviews                                                 │
│    ← genres                                                  │
│    ← directors                                               │
│    ← cast                                                    │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ Query on 'text' searches all!
                           ▼
           q=text:christopher nolan
                    matches:
           • title containing "nolan"
           • plot mentioning "christopher"
           • director "Christopher Nolan"
           • etc.
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                          │
│  • HTML5 (semantic markup)                                   │
│  • CSS3 (responsive design, flexbox, grid)                   │
│  • JavaScript (progressive enhancement)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│  APPLICATION LAYER                                           │
│  • Flask 3.0.0 (Python web framework)                        │
│  • Jinja2 (template engine)                                  │
│  • pysolr 3.9.0 (Solr Python client)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│  SEARCH ENGINE LAYER                                         │
│  • Apache Solr 9.x (search platform)                         │
│  • Lucene (underlying search library)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│  DATA LAYER                                                  │
│  • JSON (data interchange)                                   │
│  • File system (data storage)                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  DEVELOPMENT TOOLS                                           │
│  • Python 3.8+ (programming language)                        │
│  • pip (package management)                                  │
│  • requests, BeautifulSoup (web scraping)                    │
│  • Git (version control)                                     │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture (Single Server)

```
┌─────────────────────────────────────────────────────────────┐
│                    Development Machine                       │
│                       (localhost)                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Port 5000                                         │     │
│  │  Flask Application                                 │     │
│  │  python app.py                                     │     │
│  └────────────────────────────────────────────────────┘     │
│                           │                                  │
│                           │ HTTP requests                    │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Port 8983                                         │     │
│  │  Apache Solr                                       │     │
│  │  bin/solr start                                    │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  File System:                                                │
│  /Project/                                                   │
│    ├── data/movies.json          (indexed data)             │
│    ├── web/app.py                (Flask app)                │
│    ├── scrapers/                 (data collection)          │
│    └── config/managed-schema     (Solr config)              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Request/Response Cycle

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│          │  HTTP   │          │  HTTP   │          │
│ Browser  │────────▶│  Flask   │────────▶│  Solr    │
│          │ Request │          │ Query   │          │
└──────────┘         └──────────┘         └──────────┘
     ▲                    │                     │
     │                    │                     │
     │ HTML               │ JSON                │ JSON
     │                    ▼                     ▼
     │               Parse & Format       Search & Rank
     │               Render Template      Return Results
     │                    │                     │
     └────────────────────┴─────────────────────┘
              Complete rendered page
```

---

## Key Interactions

### 1. Search Flow
```
User Input → Flask Route → Solr Client → Solr Query → 
Index Search → Ranking → Results → Template → HTML → Browser
```

### 2. Faceting Flow
```
Facet Selection → Filter Queries → Solr Facet Computation → 
Facet Counts → Sidebar Display → User Refinement
```

### 3. MLT Flow
```
Document ID → MLT Handler → Term Extraction → 
Similarity Query → Ranked Results → Similar Movies Page
```

---

This architecture enables:
- ✅ Scalable search across large datasets
- ✅ Fast faceted navigation
- ✅ Accurate relevance ranking
- ✅ Intelligent recommendations
- ✅ Clean separation of concerns
- ✅ Maintainable codebase
