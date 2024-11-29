"""O'Reilly API interaction module."""
import requests
import pandas as pd
from typing import Dict, Optional, List
from datetime import datetime, date

OREILLY_API_URL = "https://learning.oreilly.com/api/v2/search/"

# Default topics for data science and AI
DEFAULT_TOPICS = [
    "data-science",
    "machine-learning",
    "artificial-intelligence",
    "data-analysis",
    "deep-learning",
    "statistics",
    "big-data"
]

# Columns to include in CSV export
CSV_COLUMNS = [
    'title',
    'authors',
    'issued',
    'publisher',
    'description',
    'topics',
    'web_url',
    'archive_id',
    'format'
]

def format_date(d: date) -> str:
    """Format date for O'Reilly API query."""
    return d.strftime("%Y-%m-%d")

def prepare_dataframe_for_export(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare DataFrame for CSV export by cleaning and organizing columns.
    
    Args:
        df: Input DataFrame from search results
        
    Returns:
        Cleaned DataFrame ready for export
    """
    if df.empty:
        return df
        
    # Create a copy to avoid modifying the original
    export_df = df.copy()
    
    # Convert authors list to comma-separated string
    if 'authors' in export_df.columns:
        export_df['authors'] = export_df['authors'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    
    # Convert topics list to comma-separated string
    if 'topics' in export_df.columns:
        export_df['topics'] = export_df['topics'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    
    # Format dates
    if 'issued' in export_df.columns:
        export_df['issued'] = pd.to_datetime(export_df['issued']).dt.strftime('%Y-%m-%d')
    
    # Select and order columns that exist in the DataFrame
    available_columns = [col for col in CSV_COLUMNS if col in export_df.columns]
    export_df = export_df[available_columns]
    
    # Clean up column names for better readability
    column_names = {
        'title': 'Title',
        'authors': 'Authors',
        'issued': 'Published Date',
        'publisher': 'Publisher',
        'description': 'Description',
        'topics': 'Topics',
        'web_url': 'URL',
        'archive_id': 'Archive ID',
        'format': 'Format'
    }
    export_df = export_df.rename(columns={col: column_names.get(col, col) for col in export_df.columns})
    
    return export_df

def search_books(
    query: str = "",
    author: Optional[str] = None,
    published_after: Optional[date] = None,
    published_before: Optional[date] = None,
    limit: int = 10,
    page: int = 0,
    fields: Optional[List[str]] = None,
    topics: Optional[List[str]] = None,
    use_default_topics: bool = True,
    export_to_csv: bool = False,
    csv_filename: str = "oreilly_books.csv"
) -> pd.DataFrame:
    """
    Search for books on O'Reilly's platform and return results as a DataFrame.
    
    Args:
        query: Search query string (default: "")
        author: Author name to search for (default: None)
        published_after: Only include books published after this date (default: None)
        published_before: Only include books published before this date (default: None)
        limit: Number of results per page (default: 10)
        page: Page number for pagination (default: 0)
        fields: List of fields to include in results (default: None, includes all)
        topics: List of topics to filter by (default: None)
        use_default_topics: Whether to use default data science/AI topics when no topics provided
        export_to_csv: Whether to export results to a CSV file (default: False)
        csv_filename: Filename for CSV export (default: "oreilly_books.csv")
    
    Returns:
        pandas DataFrame containing search results
    """
    # Build the search query
    search_query = []
    
    if query:
        search_query.append(query)
        
    if author:
        # Add author search using O'Reilly's author syntax
        # Wrap in quotes to handle multi-word author names
        search_query.append(f'author:"{author}"')
        
    # Add date filters
    if published_after:
        search_query.append(f'issued:>{format_date(published_after)}')
    if published_before:
        search_query.append(f'issued:<{format_date(published_before)}')
    
    # If no query or author specified, search all books
    if not search_query:
        search_query.append("*")
    
    params = {
        "query": " ".join(search_query),
        "limit": limit,
        "page": page,
        "formats": "book"  # Only return books
    }
    
    if fields:
        params["fields"] = ",".join(fields)
        
    # Use default topics if no topics provided and use_default_topics is True
    if topics is None and use_default_topics:
        topics = DEFAULT_TOPICS
        
    if topics:
        # Add topic filters to query using O'Reilly's topic syntax
        topic_filters = " ".join(f"topic:{topic}" for topic in topics)
        params["query"] = f"{params['query']} {topic_filters}"
    
    response = requests.get(OREILLY_API_URL, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Extract the results from the response
    results = data.get("results", [])
    
    if not results:
        return pd.DataFrame()
    
    # Convert results to DataFrame
    df = pd.DataFrame(results)
    
    # Flatten any nested JSON columns
    for col in df.select_dtypes(include=['object']):
        if isinstance(df[col].iloc[0], dict):
            nested_df = pd.json_normalize(df[col].tolist())
            # Prefix nested columns with original column name
            nested_df.columns = [f"{col}_{subcol}" for subcol in nested_df.columns]
            # Drop the original column and join the flattened columns
            df = df.drop(columns=[col]).join(nested_df)
    
    if export_to_csv:
        export_df = prepare_dataframe_for_export(df)
        export_df.to_csv(csv_filename, index=False)
    
    return df

def get_available_topics() -> List[str]:
    """
    Get a list of available topics from O'Reilly's API.
    Currently returns a curated list of common topics.
    
    Returns:
        List of topic strings
    """
    # This is a curated list of common topics
    # In a production environment, you might want to fetch this from the API
    return [
        "python",
        "javascript",
        "java",
        "data-science",
        "machine-learning",
        "web-development",
        "devops",
        "security",
        "cloud",
        "databases",
        "programming",
        "software-engineering",
        "artificial-intelligence",
        "data-analysis",
        "deep-learning",
        "statistics",
        "big-data"
    ]
