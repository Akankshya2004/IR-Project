# Interim Progress Report: Movie Information Retrieval System

## Project Information

**Project Title**: Movie Information Retrieval System with Faceted Search and Similarity Recommendations

**Course**: Information Retrieval (Course Code)  
**Semester**: Fall 2025  
**Date**: [Insert Date]

**Team Members**:
- Student 1 (ID: XXXXXXXX) - Email: student1@university.edu
- Student 2 (ID: XXXXXXXX) - Email: student2@university.edu

---

## 1. Introduction

### 1.1 Problem Description

With thousands of movies released every year and vast amounts of user-generated content across multiple platforms, finding movies that match specific preferences has become increasingly challenging. Users often struggle to discover relevant movies using simple keyword search, especially when they have multiple criteria (genre, year, rating) or want to find movies similar to ones they already enjoy.

### 1.2 Project Goals

This project aims to build an end-to-end Information Retrieval system for movie search that addresses these challenges through:

1. **Comprehensive Data Collection**: Aggregate movie information from multiple authoritative sources (IMDb, Rotten Tomatoes, Letterboxd) to provide richer metadata and diverse perspectives
2. **Robust Search Infrastructure**: Implement Apache Solr for efficient full-text search and relevance ranking
3. **Enhanced User Interface**: Develop a web-based search interface that supports both exploratory and targeted search behaviors
4. **Simple IR Feature**: Implement faceted search to enable multi-dimensional filtering (genre, year, rating)
5. **Advanced IR Feature**: Implement More Like This functionality to support similarity-based movie discovery
6. **Empirical Evaluation**: Conduct user studies to validate the effectiveness of implemented features

The system targets movie enthusiasts, casual viewers, and anyone seeking to discover movies matching specific criteria.

---

## 2. Data Sources and Acquisition

### 2.1 Selected Data Sources

We selected three complementary movie information websites:

1. **IMDb (Internet Movie Database)**
   - Rationale: Industry-standard database with comprehensive metadata
   - Data: Title, year, cast, directors, ratings, plot summaries
   - Note: Using IMDb datasets (datasets.imdbws.com) or OMDb API to comply with terms of service

2. **Rotten Tomatoes**
   - Rationale: Aggregates professional critic reviews and audience scores
   - Data: Tomatometer scores, audience ratings, critic consensus, genres
   - Focus: Review text and aggregated ratings

3. **Letterboxd**
   - Rationale: Social movie platform with community-driven content
   - Data: User ratings, community reviews, curated lists
   - Focus: User-generated review snippets and ratings

### 2.2 Scraping Strategy

**Technical Approach**:
- Python scripts using `requests`, `beautifulsoup4`, and `lxml`
- Modular design: One scraper module per site
- Respectful crawling: Rate limiting (1-2 seconds between requests), respect robots.txt
- Data normalization: Standardize rating scales (0-10), clean HTML, extract structured data

**Data Collection Process**:
1. Identify seed pages (e.g., "Top 250," "Popular Movies," "Genre Lists")
2. Extract movie list pages
3. Follow links to individual movie pages
4. Parse and extract relevant fields
5. Store in JSON format with consistent schema
6. Merge data from multiple sources, handling duplicates by title+year

**Target Dataset Size**: 150+ unique movies with rich metadata

**Ethical Considerations**:
- Comply with website terms of service
- Use official APIs where available
- Implement rate limiting to avoid server overload
- Use data for educational purposes only

### 2.3 Data Schema

Each movie document includes:
- `id`: Unique identifier (generated from title+year+source)
- `title`: Movie title
- `year`: Release year (integer)
- `genres`: List of genres (multi-valued)
- `directors`: List of directors (multi-valued)
- `cast`: List of main actors (multi-valued)
- `rating`: Normalized rating (0-10 scale)
- `num_reviews`: Review count
- `plot`: Plot summary (text)
- `reviews`: Concatenated review snippets (text)
- `url`: Link to original page
- `site`: Source website(s)

---

## 3. Indexing and Search Infrastructure

### 3.1 Technology Selection

**Apache Solr 9.x** chosen for:
- Mature, production-ready search platform
- Rich query language with faceting support
- Built-in MoreLikeThis handler
- Excellent documentation and community support
- No licensing costs (open source)

### 3.2 Schema Design

**Field Types**:
- `text_general`: Full-text search with tokenization, lowercasing, stop word removal, and Porter stemming
- `text_title`: Less aggressive tokenization for title fields
- `string`: Exact matching for facets (genres, directors, cast)
- `pint`: Integer for year and review counts
- `pfloat`: Float for ratings

**Copy Fields**:
- All searchable text copied to `text` field for unified search
- Enables single-field query with comprehensive coverage

**Key Design Decisions**:
1. **Multi-valued fields**: Genres, directors, cast support multiple values per movie
2. **Normalized ratings**: All sources converted to 0-10 scale for consistent filtering
3. **Combined text field**: Plot, reviews, title, and metadata merged for relevance ranking
4. **Facetable fields**: Genre, year, and rating configured for efficient faceted search

### 3.3 Indexing Process

1. Install and start Solr locally
2. Create `movies` collection
3. Apply custom schema via Schema API or managed-schema file
4. Index merged JSON data using Solr's post tool
5. Verify indexing through Solr Admin UI
6. Test queries and faceting functionality

---

## 4. Interface Design and Features

### 4.1 Web Application Architecture

**Backend**: Flask (Python)
- Route handlers for search, results, similar movies
- Solr query builder using `pysolr` library
- Response parsing and template rendering

**Frontend**: HTML, CSS, JavaScript
- Responsive design for desktop and mobile
- Semantic HTML for accessibility
- Progressive enhancement approach

### 4.2 Basic Search Interface

**Components**:
- Search box for keyword queries
- Results list with pagination (10 results per page)
- Result display includes:
  - Title and year
  - Rating (visual indicator)
  - Genres (tags)
  - Plot snippet or review excerpt (with highlighting)
  - Link to original source
  - Cast and director information

**Query Processing**:
- Searches across `text` field (combined title, plot, reviews, metadata)
- Default relevance ranking (TF-IDF with Solr BM25)
- Query highlighting for matched terms

### 4.3 Simple IR Feature: Faceted Search

**Implementation**:
- Genre facets: Checkbox filters for movie genres
- Year range filters: Min/max year inputs
- Rating filter: Dropdown for minimum rating threshold (7.0+, 8.0+, 9.0+)
- Multiple facets can be combined (AND logic)

**User Benefits**:
- Enables exploratory search and browsing
- Reduces cognitive load by showing available options and counts
- Supports multi-criteria decision making
- Allows iterative query refinement

**Technical Details**:
- Solr facet queries with `facet.field` parameters
- Dynamic facet counts update based on query and filters
- Client-side form submission for filter changes
- URL parameters preserve search state (bookmarkable, shareable)

### 4.4 Advanced IR Feature: More Like This

**Implementation**:
- "Find Similar Movies" button on each result
- Dedicated similar movies page
- Solr MoreLikeThis (MLT) handler configuration:
  - MLT fields: `text`, `genres`, `cast`, `directors`
  - `mlt.mindf=1`, `mlt.mintf=1`: Sensitive to term frequency
  - `mlt.maxqt=25`: Use top 25 terms for similarity

**User Benefits**:
- Serendipitous discovery beyond keyword search
- Recommendation based on content similarity
- Useful when users know what they like but can't articulate search terms
- Supports "more like this" information need

**Similarity Calculation**:
- TF-IDF vectors extracted from plot, genres, and people
- Cosine similarity or Lucene's similarity scoring
- Returns top 5-10 most similar movies

### 4.5 Additional Features

- **Sorting options**: Relevance, rating (high/low), year (new/old)
- **Query highlighting**: Matched terms highlighted in plot/review snippets
- **Responsive design**: Mobile-friendly interface
- **Clean URL structure**: RESTful routes for bookmarking

---

## 5. Evaluation Plan

### 5.1 Evaluation Goals

Compare baseline interface (basic search only) with full system (faceted search + More Like This) to answer:
1. Do advanced features improve task completion rates?
2. Do advanced features reduce time to find relevant results?
3. How do users perceive the usefulness of each feature?
4. What is overall user satisfaction?

### 5.2 Methodology

**Design**: Between-subjects experiment (baseline vs. full system)

**Participants**: 10-15 university students and movie enthusiasts

**Tasks** (5 per participant):
1. Simple known-item search ("Find movie X")
2. Faceted search ("Find sci-fi movie, 8.0+, after 2010")
3. Genre exploration ("Find 3 comedies from 1990s, 7.0+")
4. Discovery task ("Find movie similar to The Dark Knight")
5. Complex multi-criteria ("Find family animated adventure, 2019+, 7.5+")

**Metrics**:
- **Objective**: Task success rate, completion time, number of queries, pages viewed
- **Subjective**: Task difficulty, confidence, satisfaction (1-5 Likert scales)

**Analysis**:
- Chi-square tests for success rates
- Independent t-tests for time and satisfaction
- Thematic analysis of qualitative feedback

### 5.3 Expected Outcomes

**Hypotheses**:
- Full system will have higher success rates for complex tasks
- Full system will reduce time for multi-criteria searches
- Faceted search will be rated highly useful
- More Like This will be valued for discovery tasks

---

## 6. Current Progress

### 6.1 Completed Work

✅ **Week 1-2: Planning and Setup**
- Project scope definition and feature selection
- Technology stack selection (Solr, Flask, Python)
- Data source identification and ethical review

✅ **Week 3-4: Data Acquisition**
- Implemented scraper modules for three sources
- Created data merging and deduplication pipeline
- Generated sample dataset with 150+ movies
- Validated data quality and completeness

✅ **Week 5: Solr Configuration**
- Installed Solr 9.x locally
- Designed and implemented custom schema
- Created movies collection
- Indexed sample data
- Tested basic queries and faceting

✅ **Week 6-7: Web Interface Development**
- Built Flask application structure
- Implemented Solr client wrapper
- Created HTML templates (base, index, results, similar)
- Developed CSS styling (responsive design)
- Added JavaScript enhancements

✅ **Week 7: Feature Implementation**
- Implemented basic search with pagination
- Added faceted filtering (genre, year, rating)
- Integrated More Like This functionality
- Added query highlighting
- Implemented sorting options

✅ **Week 8: Testing and Refinement**
- Manual testing of all features
- Bug fixes and UI improvements
- Performance optimization
- Documentation updates

### 6.2 Current Status

The system is **functionally complete** and ready for user evaluation. All core features are implemented and tested:
- ✅ Data scraped and indexed
- ✅ Basic search working
- ✅ Faceted search operational
- ✅ More Like This integrated
- ✅ UI polished and responsive

### 6.3 Demonstration Capabilities

The system can currently:
1. Search across 150+ movies from three sources
2. Filter results by genre, year range, and minimum rating
3. Sort by relevance, rating, or year
4. Display rich movie information with highlights
5. Find similar movies using content-based similarity
6. Handle pagination for large result sets
7. Provide responsive UI for desktop and mobile

---

## 7. Next Steps

### 7.1 Week 9: User Evaluation Preparation
- [ ] Finalize evaluation materials (consent forms, task sheets)
- [ ] Recruit 10-15 participants
- [ ] Set up screen recording and logging
- [ ] Pilot test evaluation procedure

### 7.2 Week 10: User Studies
- [ ] Conduct user evaluation sessions
- [ ] Collect quantitative and qualitative data
- [ ] Record observations and feedback

### 7.3 Week 11: Analysis and Refinement
- [ ] Analyze evaluation data
- [ ] Statistical testing of hypotheses
- [ ] Identify usability issues
- [ ] Implement critical bug fixes
- [ ] Incorporate user feedback where feasible

### 7.4 Week 12: Final Report
- [ ] Write comprehensive final report
- [ ] Include evaluation results and discussion
- [ ] Reflect on limitations and future work
- [ ] Prepare demo video or presentation
- [ ] Submit final deliverables

---

## 8. Challenges and Solutions

### 8.1 Data Acquisition Challenges

**Challenge**: Some movie websites restrict automated scraping  
**Solution**: Use official APIs where available (OMDb, TMDb) and public datasets (IMDb datasets)

**Challenge**: Inconsistent data formats across sources  
**Solution**: Implement robust parsing with error handling and data normalization layer

### 8.2 Technical Challenges

**Challenge**: Solr configuration complexity  
**Solution**: Use Schema API for programmatic configuration; reference official documentation

**Challenge**: Query performance with highlighting  
**Solution**: Limit highlighted fields; use fragment size constraints

### 8.3 Design Challenges

**Challenge**: Balancing feature richness with UI simplicity  
**Solution**: Progressive disclosure - advanced filters hidden by default

**Challenge**: Making similarity meaningful to users  
**Solution**: Show similar movies with clear explanation (same genre, cast, themes)

---

## 9. Reflection and Learning

This project has provided valuable hands-on experience with:
- **Information Retrieval Concepts**: Indexing, query processing, relevance ranking, faceting, similarity
- **Search Technology**: Apache Solr configuration and optimization
- **Web Development**: Full-stack development with Flask and responsive design
- **Data Engineering**: Web scraping, data cleaning, ETL pipelines
- **User-Centered Design**: Designing IR interfaces for real tasks
- **Evaluation Methodology**: Experimental design for IR system evaluation

**Key Takeaways**:
1. Schema design significantly impacts search quality
2. Faceted search greatly enhances exploratory search
3. More Like This is powerful but requires careful tuning
4. User evaluation is essential for validating design decisions

---

## 10. References

### Technical Documentation
- Apache Solr Documentation: https://solr.apache.org/guide/
- Flask Documentation: https://flask.palletsprojects.com/
- Beautiful Soup Documentation: https://www.crummy.com/software/BeautifulSoup/

### Data Sources
- IMDb Datasets: https://datasets.imdbws.com/
- OMDb API: http://www.omdbapi.com/
- TMDb API: https://www.themoviedb.org/documentation/api

### IR Background
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
- Hearst, M. A. (2009). *Search User Interfaces*. Cambridge University Press.

### Evaluation Methodology
- Kelly, D. (2009). Methods for evaluating interactive information retrieval systems with users. *Foundations and Trends in Information Retrieval*, 3(1–2), 1-224.

---

## Appendices

### A. Project Repository Structure

```
Project/
├── README.md
├── requirements.txt
├── config/
│   ├── managed-schema
│   ├── solr-setup.md
│   └── apply_schema.sh
├── scrapers/
│   ├── scraper_utils.py
│   ├── scrape_imdb.py
│   ├── scrape_rottentomatoes.py
│   ├── scrape_letterboxd.py
│   └── merge_data.py
├── data/
│   ├── raw/
│   └── movies.json
├── web/
│   ├── app.py
│   ├── solr_client.py
│   ├── templates/
│   └── static/
├── evaluation/
│   ├── evaluation_plan.md
│   └── tasks.md
└── reports/
    └── interim_report.md
```

### B. Sample Solr Queries

**Basic Search**:
```
http://localhost:8983/solr/movies/select?q=text:inception&rows=10
```

**Faceted Search**:
```
http://localhost:8983/solr/movies/select?q=*:*&fq=genres:"Action"&fq=year:[2010 TO 2024]&fq=rating:[8.0 TO *]&facet=true&facet.field=genres
```

**More Like This**:
```
http://localhost:8983/solr/movies/mlt?q=id:movie_123&mlt.fl=text,genres,cast&rows=5
```

### C. Team Contributions

Both team members contributed equally to all aspects of the project:
- Joint planning and design decisions
- Collaborative coding (pair programming)
- Shared documentation and report writing
- Joint user evaluation planning

**Division of labor for remaining work**:
- Student 1: User evaluation facilitation, quantitative analysis
- Student 2: Qualitative analysis, final report writing
- Joint: System refinement, presentation preparation

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Status**: Interim Report - System Complete, Evaluation Pending
