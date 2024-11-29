"""O'Reilly API interaction module."""
import requests
import pandas as pd
from typing import Dict, Optional, List

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

def search_books(
    query: str,
    limit: int = 10,
    page: int = 0,
    fields: Optional[List[str]] = None,
    topics: Optional[List[str]] = None,
    use_default_topics: bool = True
) -> pd.DataFrame:
    """
    Search for books on O'Reilly's platform and return results as a DataFrame.
    
    Args:
        query: Search query string
        limit: Number of results per page (default: 10)
        page: Page number for pagination (default: 0)
        fields: List of fields to include in results (default: None, includes all)
        topics: List of topics to filter by (default: None)
        use_default_topics: Whether to use default data science/AI topics when no topics provided
    
    Returns:
        pandas DataFrame containing search results
    """
    params = {
        "query": query,
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
