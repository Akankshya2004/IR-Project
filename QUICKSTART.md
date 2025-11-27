# Quick Start Guide

This guide will help you get the Movie IR System up and running quickly.

## Prerequisites

- Python 3.8 or higher
- Apache Solr 9.x
- 2GB free disk space
- Internet connection (for scraping data)

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
cd "/Users/akankshya/Desktop/Information Retrieval/Project"
pip install -r requirements.txt
```

### 2. Install and Configure Solr

#### Option A: Using Homebrew (macOS)
```bash
brew install solr
solr start
```

#### Option B: Manual Installation
```bash
# Download Solr 9.x from https://solr.apache.org/downloads.html
tar xzf solr-9.x.x.tgz
cd solr-9.x.x
bin/solr start
```

### 3. Create Solr Collection and Apply Schema

```bash
# Create the movies collection
bin/solr create -c movies

# Apply the schema
cd "/Users/akankshya/Desktop/Information Retrieval/Project/config"
chmod +x apply_schema.sh
./apply_schema.sh
```

Verify in browser: http://localhost:8983/solr/#/movies

### 4. Scrape and Prepare Data

```bash
cd "/Users/akankshya/Desktop/Information Retrieval/Project/scrapers"

# Run each scraper
python scrape_imdb.py
python scrape_rottentomatoes.py
python scrape_letterboxd.py

# Merge data into single file
python merge_data.py
```

This will create `data/movies.json` with ~150 movies.

### 5. Index Data in Solr

From your Solr installation directory:

```bash
bin/post -c movies "/Users/akankshya/Desktop/Information Retrieval/Project/data/movies.json"
```

Verify indexing:
- Open: http://localhost:8983/solr/#/movies/query
- Click "Execute Query"
- You should see movie documents in the response

### 6. Run the Web Application

```bash
cd "/Users/akankshya/Desktop/Information Retrieval/Project/web"
python app.py
```

Open your browser to: **http://localhost:5000**

## Using the Quick Start Script

Alternatively, use the automated setup script:

```bash
cd "/Users/akankshya/Desktop/Information Retrieval/Project"
chmod +x run.sh
./run.sh
```

This script will:
1. Check prerequisites
2. Install dependencies
3. Verify Solr is running
4. Run scrapers if needed
5. Check data indexing
6. Start the web application

## Testing the System

### Test Basic Search
1. Go to http://localhost:5000
2. Search for "inception"
3. You should see results

### Test Faceted Search
1. Click "Advanced Filters"
2. Select genre "Action"
3. Set year range: 2010-2020
4. Set minimum rating: 8.0
5. Click "Search" or "Apply Filters"

### Test More Like This
1. Search for any movie
2. Click "Find Similar Movies" on a result
3. You should see similar movies based on plot, genre, and cast

## Troubleshooting

### Solr Not Running
```bash
# Check status
curl http://localhost:8983/solr/

# Start Solr
cd <solr-directory>
bin/solr start
```

### Port 8983 Already in Use
```bash
# Find and kill process
lsof -ti:8983 | xargs kill -9

# Or start Solr on different port
bin/solr start -p 8984
# Then update solr_client.py to use new port
```

### No Movies in Search Results
```bash
# Check if documents are indexed
curl "http://localhost:8983/solr/movies/select?q=*:*&rows=0"

# Look for "numFound" in response
# If 0, re-run indexing step
```

### Flask Port 5000 in Use
```bash
# Edit web/app.py, change last line:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

Once the system is running:

1. **Explore Features**
   - Try different search queries
   - Use faceted filters
   - Explore similar movies

2. **Review Documentation**
   - `README.md` - Project overview
   - `config/solr-setup.md` - Solr configuration details
   - `evaluation/evaluation_plan.md` - User study design

3. **Prepare for Evaluation**
   - Review `evaluation/tasks.md`
   - Recruit participants
   - Conduct user studies

4. **Customize**
   - Add more data sources in `scrapers/`
   - Modify UI in `web/templates/`
   - Adjust Solr schema in `config/managed-schema`

## Useful Commands

```bash
# Check Solr status
curl http://localhost:8983/solr/admin/info/system

# View indexed documents
curl "http://localhost:8983/solr/movies/select?q=*:*&rows=10"

# Delete all documents (start fresh)
curl "http://localhost:8983/solr/movies/update?commit=true" \
  -H "Content-Type: text/xml" \
  --data-binary '<delete><query>*:*</query></delete>'

# Stop Solr
bin/solr stop

# Restart Flask with auto-reload
python app.py  # Already has debug=True
```

## Getting Help

- **Solr Documentation**: https://solr.apache.org/guide/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Project README**: `README.md`
- **Solr Admin UI**: http://localhost:8983/solr/

## System Requirements

- **Minimum**: 4GB RAM, 2GB disk space
- **Recommended**: 8GB RAM, 5GB disk space
- **Browser**: Chrome, Firefox, Safari (latest versions)
- **OS**: macOS, Linux, or Windows with WSL

Enjoy using the Movie IR System! 🎬
