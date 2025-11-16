from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import scoring
from datetime import datetime
import os
from config import Config
from file_parser import extract_text_from_file, get_file_category

# Define search schema
schema = Schema(
    filename=TEXT(stored=True),
    filepath=ID(stored=True, unique=True),
    content=TEXT(stored=False),
    category=TEXT(stored=True),
    upload_date=DATETIME(stored=True),
    preview=TEXT(stored=True)
)

def get_or_create_index():
    """Get existing index or create new one"""
    if not os.path.exists(Config.INDEX_DIR):
        os.makedirs(Config.INDEX_DIR)
    
    if exists_in(Config.INDEX_DIR):
        return open_dir(Config.INDEX_DIR)
    else:
        return create_in(Config.INDEX_DIR, schema)

def index_document(filepath, filename):
    """Index a single document"""
    try:
        # Extract text content
        content = extract_text_from_file(filepath)
        category = get_file_category(filename)
        preview = content[:200] if content else "No preview available"
        
        print(f"Indexing: {filename}, Category: {category}")
        
        # Add to index
        ix = get_or_create_index()
        writer = ix.writer()
        
        writer.update_document(
            filename=filename,
            filepath=filepath,
            content=content,
            category=category,
            upload_date=datetime.now(),
            preview=preview
        )
        
        writer.commit()
        print(f"Successfully indexed: {filename}")
        return True, "Document indexed successfully"
    
    except Exception as e:
        print(f"Error indexing document: {str(e)}")
        return False, f"Error indexing document: {str(e)}"

def search_documents(query_str, category_filter=None, limit=20):
    """Search indexed documents"""
    try:
        ix = get_or_create_index()
        
        with ix.searcher(weighting=scoring.BM25F()) as searcher:
            # Parse the query
            parser = MultifieldParser(["filename", "content"], schema=ix.schema)
            query = parser.parse(query_str)
            
            # Search without category filter first
            all_results = searcher.search(query, limit=limit * 2)
            
            # Apply category filter after search
            search_results = []
            for hit in all_results:
                # If filter is applied and doesn't match, skip
                if category_filter and category_filter != 'All':
                    if hit['category'] != category_filter:
                        continue
                
                search_results.append({
                    'filename': hit['filename'],
                    'filepath': hit['filepath'],
                    'category': hit['category'],
                    'upload_date': hit['upload_date'].strftime('%Y-%m-%d %H:%M'),
                    'preview': hit['preview'],
                    'score': hit.score
                })
                
                # Limit results after filtering
                if len(search_results) >= limit:
                    break
            
            print(f"Search query: {query_str}, Filter: {category_filter}, Results: {len(search_results)}")
            return search_results
    
    except Exception as e:
        print(f"Search error: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_all_categories():
    """Get list of all categories in the index"""
    try:
        ix = get_or_create_index()
        with ix.searcher() as searcher:
            categories = set()
            for doc in searcher.all_stored_fields():
                cat = doc.get('category', 'General')
                if cat:
                    categories.add(cat)
            
            result = sorted(list(categories))
            print(f"Available categories: {result}")
            return result
    except Exception as e:
        print(f"Error getting categories: {e}")
        return ['General', 'Reports', 'Campaigns', 'Presentations', 'Documentation']
