"""
Solr client interface for movie search.
Provides methods to query Solr and parse results.
"""

import pysolr
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode


class SolrClient:
    """Interface for querying Solr movies collection."""
    
    def __init__(self, solr_url: str = 'http://localhost:8983/solr/movies'):
        """
        Initialize Solr client.
        
        Args:
            solr_url: URL of the Solr movies collection
        """
        self.solr = pysolr.Solr(solr_url, always_commit=True, timeout=10)
        self.solr_url = solr_url
    
    def search(
        self,
        query: str = '*:*',
        filters: Optional[Dict[str, Any]] = None,
        facets: Optional[List[str]] = None,
        sort: Optional[str] = None,
        start: int = 0,
        rows: int = 10,
        highlight: bool = False
    ) -> Dict:
        """
        Perform a search query on Solr.
        
        Args:
            query: Main search query (searches the 'text' field by default)
            filters: Dictionary of filter queries (fq parameters)
            facets: List of fields to facet on
            sort: Sort order (e.g., 'rating desc', 'year asc')
            start: Start position for pagination
            rows: Number of results to return
            highlight: Whether to enable highlighting
            
        Returns:
            Dictionary with results, facets, and metadata
        """
        # Build query parameters
        params = {
            'q': f'text:{query}' if query != '*:*' else query,
            'start': start,
            'rows': rows,
            'fl': 'id,title,year,rating,genres,directors,cast,plot,reviews,url,site,num_reviews'
        }
        
        # Add sort
        if sort:
            params['sort'] = sort
        
        # Add filter queries
        if filters:
            fq_list = []
            for field, value in filters.items():
                if isinstance(value, list):
                    # Multiple values for same field (OR)
                    or_clauses = [f'{field}:"{v}"' for v in value]
                    fq_list.append(f"({' OR '.join(or_clauses)})")
                elif isinstance(value, tuple) and len(value) == 2:
                    # Range query (e.g., year:[2000 TO 2024])
                    fq_list.append(f'{field}:[{value[0]} TO {value[1]}]')
                else:
                    fq_list.append(f'{field}:"{value}"')
            params['fq'] = fq_list
        
        # Add faceting
        if facets:
            params['facet'] = 'true'
            params['facet.field'] = facets
            params['facet.mincount'] = 1
            params['facet.limit'] = 20
        
        # Add highlighting
        if highlight:
            params['hl'] = 'true'
            params['hl.fl'] = 'plot,reviews'
            params['hl.simple.pre'] = '<mark>'
            params['hl.simple.post'] = '</mark>'
            params['hl.fragsize'] = 200
        
        # Execute search
        try:
            results = self.solr.search(**params)
            
            # Parse response
            response = {
                'docs': list(results.docs),
                'num_found': results.hits,
                'start': start,
                'rows': rows,
                'query': query,
                'filters': filters or {},
                'facets': self._parse_facets(results.facets) if facets else {},
                'highlighting': results.highlighting if highlight else {}
            }
            
            return response
            
        except Exception as e:
            print(f"Solr search error: {e}")
            return {
                'docs': [],
                'num_found': 0,
                'start': 0,
                'rows': rows,
                'error': str(e)
            }
    
    def more_like_this(
        self,
        doc_id: str,
        mlt_fields: List[str] = None,
        rows: int = 5
    ) -> Dict:
        """
        Find similar movies using MoreLikeThis.
        
        Args:
            doc_id: ID of the document to find similar items for
            mlt_fields: Fields to use for similarity (default: text, genres, cast)
            rows: Number of similar movies to return
            
        Returns:
            Dictionary with similar movies
        """
        if mlt_fields is None:
            mlt_fields = ['text', 'genres', 'cast', 'directors']
        
        params = {
            'q': f'id:{doc_id}',
            'mlt': 'true',
            'mlt.fl': ','.join(mlt_fields),
            'mlt.mindf': 1,
            'mlt.mintf': 1,
            'mlt.minwl': 3,
            'mlt.maxqt': 25,
            'mlt.count': rows,
            'fl': 'id,title,year,rating,genres,directors,cast,plot,url,site'
        }
        
        try:
            results = self.solr.search(**params)
            
            # Extract MLT results
            similar_docs = []
            if hasattr(results, 'moreLikeThis') and results.moreLikeThis:
                mlt_results = results.moreLikeThis.get(doc_id, [])
                similar_docs = list(mlt_results)
            
            return {
                'docs': similar_docs,
                'num_found': len(similar_docs),
                'source_id': doc_id
            }
            
        except Exception as e:
            print(f"MoreLikeThis error: {e}")
            return {
                'docs': [],
                'num_found': 0,
                'error': str(e)
            }
    
    def get_by_id(self, doc_id: str) -> Optional[Dict]:
        """
        Get a specific movie by ID.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Movie document or None if not found
        """
        try:
            results = self.solr.search(q=f'id:{doc_id}', rows=1)
            if results.docs:
                return results.docs[0]
            return None
        except Exception as e:
            print(f"Get by ID error: {e}")
            return None
    
    def _parse_facets(self, facet_data: Dict) -> Dict:
        """
        Parse facet data from Solr response.
        
        Args:
            facet_data: Raw facet data from Solr
            
        Returns:
            Parsed facet dictionary
        """
        if not facet_data or 'facet_fields' not in facet_data:
            return {}
        
        parsed_facets = {}
        for field, values in facet_data['facet_fields'].items():
            # Solr returns facets as [value1, count1, value2, count2, ...]
            facet_list = []
            for i in range(0, len(values), 2):
                if i + 1 < len(values):
                    facet_list.append({
                        'value': values[i],
                        'count': values[i + 1]
                    })
            parsed_facets[field] = facet_list
        
        return parsed_facets
    
    def get_facet_values(self, field: str, limit: int = 20) -> List[Dict]:
        """
        Get all unique values for a facet field.
        
        Args:
            field: Field to get facet values for
            limit: Maximum number of values to return
            
        Returns:
            List of facet values with counts
        """
        try:
            results = self.solr.search(
                q='*:*',
                rows=0,
                facet='true',
                facet_field=field,
                facet_mincount=1,
                facet_limit=limit
            )
            return self._parse_facets(results.facets).get(field, [])
        except Exception as e:
            print(f"Get facet values error: {e}")
            return []
    
    def stats(self) -> Dict:
        """
        Get collection statistics.
        
        Returns:
            Dictionary with collection stats
        """
        try:
            results = self.solr.search(q='*:*', rows=0)
            return {
                'total_docs': results.hits,
                'status': 'ok'
            }
        except Exception as e:
            return {
                'total_docs': 0,
                'status': 'error',
                'error': str(e)
            }
