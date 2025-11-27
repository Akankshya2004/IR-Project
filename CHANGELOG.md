# Changelog

All notable changes and features of this project are documented here.

## [1.0.0] - 2025-11-27

### Initial Release

#### Data Acquisition
- ✅ Created modular scraper architecture with `scraper_utils.py`
- ✅ Implemented IMDb scraper (`scrape_imdb.py`)
- ✅ Implemented Rotten Tomatoes scraper (`scrape_rottentomatoes.py`)
- ✅ Implemented Letterboxd scraper (`scrape_letterboxd.py`)
- ✅ Built data merger with intelligent deduplication (`merge_data.py`)
- ✅ Added rating normalization (0-10 scale)
- ✅ Implemented respectful crawling (rate limiting)
- ✅ Created sample data generation (for demonstration)

#### Solr Integration
- ✅ Designed complete Solr schema (`managed-schema`)
  - 13 fields covering all movie metadata
  - Text analysis with stemming and stop words
  - Multi-valued fields for genres, directors, cast
  - Copy fields for unified text search
- ✅ Created schema application script (`apply_schema.sh`)
- ✅ Wrote comprehensive Solr setup guide (`solr-setup.md`)
- ✅ Configured for MoreLikeThis functionality

#### Web Application
- ✅ Built Flask application structure (`app.py`)
  - Home route with search form
  - Search route with faceting support
  - Similar movies route (MLT)
  - API endpoints for stats and autocomplete
- ✅ Implemented Solr client wrapper (`solr_client.py`)
  - Search with filters and facets
  - MoreLikeThis queries
  - Result parsing and formatting
  - Error handling
- ✅ Created template system
  - Base layout with navigation
  - Home page with advanced filters
  - Results page with sidebar facets
  - Similar movies page
  - Error pages
- ✅ Designed responsive CSS (`style.css`)
  - Modern, clean interface
  - Mobile-friendly layout
  - Color scheme and typography
  - Card-based result display
- ✅ Added JavaScript enhancements (`main.js`)
  - Scroll to top button
  - Keyboard shortcuts
  - Autocomplete support (optional)

#### Features

**Basic Search**
- ✅ Full-text search across title, plot, reviews
- ✅ Relevance ranking (Solr default TF-IDF/BM25)
- ✅ Result pagination (10 per page)
- ✅ Query highlighting in snippets
- ✅ Rich result display with metadata

**Simple IR Feature: Faceted Search**
- ✅ Genre facets with checkboxes
- ✅ Year range filter (min/max)
- ✅ Rating filter (dropdown)
- ✅ Multiple facets combinable (AND logic)
- ✅ Dynamic facet counts
- ✅ Sorting options (relevance, rating, year)

**Advanced IR Feature: More Like This**
- ✅ Similarity-based recommendations
- ✅ Uses plot, genres, cast, directors
- ✅ Configurable similarity parameters
- ✅ Dedicated similar movies page
- ✅ Source movie context display

#### Evaluation
- ✅ Complete evaluation plan (`evaluation_plan.md`)
  - Between-subjects design
  - 5 evaluation tasks
  - Quantitative and qualitative metrics
  - Analysis methodology
- ✅ User study materials (`tasks.md`)
  - Participant instructions
  - Task descriptions with success criteria
  - Questionnaires (Likert scales)
  - Recording sheets
  - Debriefing script

#### Documentation
- ✅ Project README with overview
- ✅ Quick start guide (`QUICKSTART.md`)
- ✅ Developer guide (`DEVELOPMENT.md`)
- ✅ Project summary (`PROJECT_SUMMARY.md`)
- ✅ Interim progress report (`interim_report.md`)
  - 10+ pages covering all aspects
  - Ready for submission
- ✅ Solr setup instructions
- ✅ Code comments and docstrings

#### Infrastructure
- ✅ Python requirements file (`requirements.txt`)
- ✅ Automated setup script (`run.sh`)
- ✅ Git ignore configuration (`.gitignore`)
- ✅ Directory structure with .gitkeep files
- ✅ Executable permissions on scripts

### Technical Details

#### Dependencies
- Flask 3.0.0 (web framework)
- pysolr 3.9.0 (Solr client)
- requests 2.31.0 (HTTP)
- beautifulsoup4 4.12.2 (HTML parsing)
- lxml 4.9.3 (XML/HTML parser)

#### Solr Configuration
- Schema version: 1.6
- Field types: text_general, text_title, string, pint, pfloat
- Analyzers: StandardTokenizer, LowerCase, StopFilter, PorterStem
- Special features: MoreLikeThis, Highlighting, Faceting

#### Browser Support
- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

### File Count
- Python files: 7
- HTML templates: 5
- CSS files: 1
- JavaScript files: 1
- Markdown docs: 8
- Configuration files: 3
- Shell scripts: 2

**Total lines of code**: ~3,500+

### Testing Status
- ✅ Manual testing completed
- ✅ All routes functional
- ✅ Solr queries working
- ✅ UI responsive on desktop and mobile
- ✅ Error handling in place
- ⏳ User evaluation pending

### Known Limitations
- Sample data only (scrapers generate demo data)
- No authentication/user accounts
- No administrative interface
- Single-server deployment
- No caching layer
- Limited to 150 movies initially

### Future Enhancements (Potential)
- [ ] Real data from APIs (OMDb, TMDb)
- [ ] User accounts and favorites
- [ ] Personalized recommendations
- [ ] Advanced filters (runtime, language, country)
- [ ] Watchlist functionality
- [ ] Movie ratings by users
- [ ] Social features (reviews, lists)
- [ ] Query suggestions/autocomplete
- [ ] Result clustering
- [ ] Spell correction
- [ ] Multi-language support
- [ ] Export functionality
- [ ] API for programmatic access
- [ ] Docker deployment
- [ ] Automated testing suite
- [ ] Performance monitoring

---

## Version History

### Version 1.0.0 - Initial Release (Current)
- Complete IR system ready for demo
- All core features implemented
- Documentation complete
- Ready for user evaluation

---

## Acknowledgments

Built for Information Retrieval course project on the topic "Movies".

Technologies used:
- Apache Solr 9.x
- Python 3.8+
- Flask web framework
- HTML5, CSS3, JavaScript
- Bootstrap concepts (custom implementation)

Inspired by:
- Google Scholar search interface (faceting)
- IMDb website (movie display)
- Spotify recommendations (similarity)
- Modern web design principles

---

_Last updated: November 27, 2025_
