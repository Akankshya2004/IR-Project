# Apache Solr Setup Instructions

## Installation

### macOS (using Homebrew)

```bash
brew install solr
```

### Manual Installation (All platforms)

1. Download Solr 9.x from https://solr.apache.org/downloads.html
2. Extract the archive:
   ```bash
   tar xzf solr-9.x.x.tgz
   cd solr-9.x.x
   ```

## Starting Solr

```bash
bin/solr start
```

Solr will start on http://localhost:8983

To check status:
```bash
bin/solr status
```

## Creating the Movies Collection

```bash
bin/solr create -c movies
```

This creates a new collection named "movies" with default configuration.

## Applying the Schema

### Method 1: Using Schema API (Recommended)

After creating the collection, apply the schema using the Schema API:

```bash
# Navigate to the project config directory
cd /path/to/Project/config

# Run the schema setup script
./apply_schema.sh
```

Or manually with curl:

```bash
# Add field types
curl -X POST -H 'Content-type:application/json' \
  http://localhost:8983/solr/movies/schema -d '{
  "add-field-type": {
    "name": "text_general",
    "class": "solr.TextField",
    "positionIncrementGap": "100",
    "analyzer": {
      "tokenizer": {"class": "solr.StandardTokenizerFactory"},
      "filters": [
        {"class": "solr.LowerCaseFilterFactory"},
        {"class": "solr.StopFilterFactory"},
        {"class": "solr.PorterStemFilterFactory"}
      ]
    }
  }
}'

# Add fields (see apply_schema.sh for complete commands)
```

### Method 2: Replace managed-schema File

1. Stop Solr:
   ```bash
   bin/solr stop
   ```

2. Copy the managed-schema file:
   ```bash
   cp /path/to/Project/config/managed-schema \
      server/solr/movies/conf/managed-schema
   ```

3. Start Solr:
   ```bash
   bin/solr start
   ```

## Indexing Data

Once your schema is configured and you have scraped data:

```bash
bin/post -c movies /path/to/Project/data/movies.json
```

Check the admin UI to verify documents were indexed:
http://localhost:8983/solr/#/movies/query

## Testing Queries

### Basic Query
```
http://localhost:8983/solr/movies/select?q=text:batman&rows=10
```

### Faceted Query
```
http://localhost:8983/solr/movies/select?
  q=*:*&
  facet=true&
  facet.field=genres&
  facet.field=year&
  rows=10
```

### More Like This
```
http://localhost:8983/solr/movies/mlt?
  q=id:movie_12345&
  mlt.fl=text,genres,cast&
  mlt.mindf=1&
  mlt.mintf=1&
  rows=5
```

### Query with Highlighting
```
http://localhost:8983/solr/movies/select?
  q=text:inception&
  hl=true&
  hl.fl=plot,reviews&
  rows=10
```

## Common Issues

### Port Already in Use
```bash
# Find and kill process on port 8983
lsof -ti:8983 | xargs kill -9

# Or start on different port
bin/solr start -p 8984
```

### Schema Changes Not Applied
```bash
# Reload the collection
bin/solr reload -c movies
```

### Clear All Data
```bash
# Delete all documents
curl http://localhost:8983/solr/movies/update?commit=true \
  -H "Content-Type: text/xml" \
  --data-binary '<delete><query>*:*</query></delete>'
```

## Stopping Solr

```bash
bin/solr stop
```

## Admin UI

Access the Solr Admin UI at:
http://localhost:8983/solr/

This provides:
- Query interface for testing
- Schema browser
- Index statistics
- Log viewer
