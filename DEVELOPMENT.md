# Development Guide

This guide provides detailed information for extending and customizing the Movie IR System.

## Project Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Web Browser                          │
│                  (HTML/CSS/JavaScript)                   │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Flask Application                       │
│                    (app.py)                              │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Routes: /, /search, /similar/<id>              │   │
│  │  Templates: Jinja2 rendering                     │   │
│  │  Static files: CSS, JS                           │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │ pysolr
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Solr Client                             │
│                (solr_client.py)                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Query building & result parsing                 │   │
│  │  Faceting, MLT, highlighting                     │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/JSON
                     │
┌────────────────────▼────────────────────────────────────┐
│                   Apache Solr                            │
│              (localhost:8983/solr)                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  movies Collection                               │   │
│  │  - Indexing & storage                            │   │
│  │  - Query processing                              │   │
│  │  - Ranking & scoring                             │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

## Code Structure

### Scrapers (`scrapers/`)

**scraper_utils.py**: Common utilities
- `ScraperUtils`: HTTP requests, text cleaning, rating normalization
- `create_movie_document()`: Standardized document creation

**scrape_*.py**: Site-specific scrapers
- Each scraper has its own class
- `scrape_*_movies()`: Main scraping method
- `save_data()`: Outputs JSON

**merge_data.py**: Data consolidation
- `DataMerger`: Handles deduplication
- Groups by (title, year)
- Merges fields intelligently

### Web Application (`web/`)

**app.py**: Flask routes
- `index()`: Home page
- `search()`: Main search with faceting
- `similar_movies()`: More Like This
- Template filters: `truncate_list`, `join_with_comma`

**solr_client.py**: Solr interface
- `SolrClient.search()`: Full-text search with filters
- `SolrClient.more_like_this()`: Similarity search
- `SolrClient.get_by_id()`: Fetch single document
- `SolrClient.get_facet_values()`: Get facet options

**templates/**: Jinja2 templates
- `base.html`: Base layout
- `index.html`: Home/search page
- `results.html`: Search results with faceting
- `similar.html`: Similar movies display
- `error.html`: Error pages

**static/**: Frontend assets
- `css/style.css`: All styles
- `js/main.js`: JavaScript enhancements

## Adding New Features

### 1. Add a New Data Source

Create `scrapers/scrape_newsource.py`:

```python
from scraper_utils import ScraperUtils, create_movie_document

class NewSourceScraper:
    def __init__(self, output_file='../data/raw/newsource_movies.json'):
        self.output_file = output_file
        self.movies = []
        self.utils = ScraperUtils()
    
    def scrape_movies(self, limit=50):
        # Your scraping logic here
        pass
    
    def save_data(self):
        documents = []
        for movie in self.movies:
            doc = create_movie_document(
                title=movie['title'],
                year=movie['year'],
                site='newsource',
                url=movie['url'],
                # ... other fields
            )
            documents.append(doc)
        
        # Save to JSON
        import json, os
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    scraper = NewSourceScraper()
    scraper.scrape_movies(limit=50)
    scraper.save_data()
```

Update `merge_data.py` to include new source:
```python
sources = [
    '../data/raw/imdb_movies.json',
    '../data/raw/rottentomatoes_movies.json',
    '../data/raw/letterboxd_movies.json',
    '../data/raw/newsource_movies.json'  # Add this
]
```

### 2. Add a New Field to Schema

Edit `config/managed-schema`:

```xml
<!-- Add new field -->
<field name="awards" type="text_general" indexed="true" stored="true" multiValued="true" />

<!-- Add to copy field if searchable -->
<copyField source="awards" dest="text"/>
```

Or use Schema API:
```bash
curl -X POST -H 'Content-type:application/json' \
  http://localhost:8983/solr/movies/schema -d '{
  "add-field": {
    "name": "awards",
    "type": "text_general",
    "stored": true,
    "indexed": true,
    "multiValued": true
  }
}'
```

Update scrapers to populate new field.

### 3. Add a New Route

In `web/app.py`:

```python
@app.route('/advanced-search')
def advanced_search():
    """New advanced search page."""
    # Get parameters
    title = request.args.get('title', '')
    director = request.args.get('director', '')
    cast = request.args.get('cast', '')
    
    # Build complex query
    query_parts = []
    if title:
        query_parts.append(f'title:"{title}"')
    if director:
        query_parts.append(f'directors:"{director}"')
    if cast:
        query_parts.append(f'cast:"{cast}"')
    
    query = ' AND '.join(query_parts) if query_parts else '*:*'
    
    # Execute search
    results = solr_client.search(query=query, rows=20)
    
    return render_template('advanced_search.html', results=results)
```

Create `web/templates/advanced_search.html`.

### 4. Add a New Facet

In `web/app.py`, update the search route:

```python
# Add director facet
results = solr_client.search(
    query=query,
    filters=filters,
    facets=['genres', 'year', 'directors'],  # Add directors
    sort=sort,
    start=start,
    rows=RESULTS_PER_PAGE,
    highlight=True
)
```

In `web/templates/results.html`, add facet display:

```html
<!-- Director facets -->
{% if facets.directors %}
<div class="facet-group">
    <h4>Directors</h4>
    {% for director in facets.directors[:10] %}
    <label class="facet-item">
        <input type="checkbox" name="directors" value="{{ director.value }}">
        <span>{{ director.value }}</span>
        <span class="facet-count">{{ director.count }}</span>
    </label>
    {% endfor %}
</div>
{% endif %}
```

### 5. Customize Ranking

Modify Solr query in `solr_client.py`:

```python
def search(self, query, boost_recent=False, **kwargs):
    params = {
        'q': f'text:{query}' if query != '*:*' else query,
        # ... other params
    }
    
    # Boost recent movies
    if boost_recent:
        params['boost'] = 'recip(ms(NOW,year),3.16e-11,1,1)'
    
    # Custom field weights
    params['qf'] = 'title^2.0 plot^1.0 reviews^0.5'
    
    results = self.solr.search(**params)
    # ...
```

## Testing

### Unit Tests

Create `tests/test_scrapers.py`:

```python
import unittest
from scrapers.scraper_utils import ScraperUtils

class TestScraperUtils(unittest.TestCase):
    def test_normalize_rating(self):
        utils = ScraperUtils()
        self.assertEqual(utils.normalize_rating(5.0, 10.0), 5.0)
        self.assertEqual(utils.normalize_rating(4.0, 5.0), 8.0)
        self.assertEqual(utils.normalize_rating(85, 100), 8.5)
    
    def test_extract_year(self):
        utils = ScraperUtils()
        self.assertEqual(utils.extract_year("Released in 2020"), 2020)
        self.assertEqual(utils.extract_year("1995 movie"), 1995)
        self.assertIsNone(utils.extract_year("no year here"))

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m pytest tests/
```

### Integration Testing

Test full pipeline:

```bash
# 1. Scrape data
cd scrapers
python scrape_imdb.py

# 2. Check output
cat ../data/raw/imdb_movies.json | jq '.[0]'

# 3. Index in Solr
bin/post -c movies ../data/movies.json

# 4. Test query
curl "http://localhost:8983/solr/movies/select?q=inception"

# 5. Test web interface
cd ../web
python app.py
# Open http://localhost:5000
```

## Performance Optimization

### Solr Optimization

**1. Commit Strategy**
```xml
<!-- In solrconfig.xml -->
<autoCommit>
  <maxTime>15000</maxTime>
  <openSearcher>false</openSearcher>
</autoCommit>
```

**2. Cache Configuration**
```xml
<query>
  <filterCache size="512" initialSize="512" />
  <queryResultCache size="512" initialSize="512" />
  <documentCache size="512" initialSize="512" />
</query>
```

**3. Query Optimization**
- Use filter queries (fq) for facets
- Limit returned fields (fl parameter)
- Use pagination (start, rows)

### Flask Optimization

**1. Enable Caching**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/search')
@cache.cached(timeout=300, query_string=True)
def search():
    # ...
```

**2. Gzip Compression**
```python
from flask_compress import Compress

Compress(app)
```

**3. Production Server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Debugging

### Solr Debugging

**Enable debug output:**
```python
results = solr_client.search(
    query=query,
    debug='true'  # Add this
)
```

**Check Solr logs:**
```bash
tail -f <solr-dir>/server/logs/solr.log
```

**Test queries in Admin UI:**
http://localhost:8983/solr/#/movies/query

### Flask Debugging

**Enable detailed errors:**
```python
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
```

**Use Flask debugger:**
```python
from flask import Flask
app = Flask(__name__)
app.debug = True  # Enables interactive debugger
```

**Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.debug('Search query: %s', query)
```

## Deployment

### Production Checklist

- [ ] Change Flask secret key
- [ ] Disable debug mode
- [ ] Use production WSGI server (gunicorn)
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure Solr for production
- [ ] Set up monitoring
- [ ] Implement rate limiting
- [ ] Add error tracking (Sentry)
- [ ] Backup Solr data regularly

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "web.app:app"]
```

Create `docker-compose.yml`:
```yaml
version: '3'
services:
  solr:
    image: solr:9
    ports:
      - "8983:8983"
    volumes:
      - ./config:/opt/solr/server/solr/configsets/movies
  
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - solr
    environment:
      - SOLR_URL=http://solr:8983/solr/movies
```

## Common Issues and Solutions

### Issue: Schema mismatch after update
**Solution:**
```bash
bin/solr delete -c movies
bin/solr create -c movies
cd config && ./apply_schema.sh
# Re-index data
```

### Issue: Slow queries
**Solution:**
- Check query explain: add `debugQuery=true`
- Add filter queries for facets
- Optimize Solr cache settings
- Consider field type optimization

### Issue: Memory issues with large datasets
**Solution:**
- Increase Solr heap: `bin/solr start -m 2g`
- Use streaming for scraping
- Batch indexing with commit intervals

## Contributing

When adding features:
1. Follow existing code style
2. Add docstrings to functions
3. Update relevant documentation
4. Test thoroughly
5. Update CHANGELOG.md

## Resources

- **Solr Ref Guide**: https://solr.apache.org/guide/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Jinja2 Templates**: https://jinja.palletsprojects.com/
- **Bootstrap CSS**: https://getbootstrap.com/ (if you want to use it)
- **IR Textbook**: Manning et al., "Introduction to Information Retrieval"

Happy coding! 🚀
