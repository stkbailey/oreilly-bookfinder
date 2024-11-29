"""Command line interface for O'Reilly Bookfinder."""
import click
from typing import List, Optional
from datetime import datetime, date
from . import api

def parse_date(ctx, param, value) -> Optional[date]:
    """Parse date from string in YYYY-MM-DD format."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise click.BadParameter("Date must be in YYYY-MM-DD format")

@click.group()
def cli():
    """Search and explore O'Reilly books."""
    pass

@cli.command()
@click.argument('query', required=False)
@click.option('--author', '-a', help='Search by author name')
@click.option('--after', callback=parse_date, help='Only show books published after date (YYYY-MM-DD)')
@click.option('--before', callback=parse_date, help='Only show books published before date (YYYY-MM-DD)')
@click.option('--limit', '-l', default=10, help='Number of results to return')
@click.option('--page', '-p', default=0, help='Page number for pagination')
@click.option('--output', '-o', type=click.Path(), help='Save results to CSV file')
@click.option('--topic', '-t', multiple=True, help='Filter by topic (can be used multiple times)')
@click.option('--list-topics', is_flag=True, help='List available topics')
@click.option('--all-topics', is_flag=True, help='Search all topics (disable default data science filter)')
def search(
    query: str,
    author: str,
    after: date,
    before: date,
    limit: int,
    page: int,
    output: str,
    topic: List[str],
    list_topics: bool,
    all_topics: bool
):
    """
    Search for books by title, content, or author. By default, searches only data science and AI topics.
    
    Examples:
        # Search by query
        bookfinder search "machine learning"
        
        # Search by author
        bookfinder search --author "Joel Grus"
        
        # Search with date range
        bookfinder search "python" --after 2023-01-01 --before 2024-01-01
        
        # Search with both query and author
        bookfinder search "data science" --author "Joel Grus"
        
        # Search with custom topics
        bookfinder search "python" --topic web-development
        
        # Export results to CSV
        bookfinder search "python" --output results.csv
    """
    if list_topics:
        topics = api.get_available_topics()
        click.echo("\nAvailable topics:")
        for t in topics:
            click.echo(f"- {t}")
        return
        
    if not query and not author:
        click.echo("Please provide either a search query or an author name.")
        return
        
    try:
        df = api.search_books(
            query=query or "", 
            author=author,
            published_after=after,
            published_before=before,
            limit=limit, 
            page=page, 
            topics=list(topic) if topic else None,
            use_default_topics=not all_topics
        )
        
        if df.empty:
            click.echo("No results found.")
            return
            
        # Display basic information about each book
        for _, row in df.iterrows():
            click.echo(f"\nTitle: {row.get('title', 'N/A')}")
            click.echo(f"Authors: {', '.join(row.get('authors', []))}")
            click.echo(f"Published: {row.get('issued', 'N/A')}")
            click.echo(f"URL: {row.get('web_url', 'N/A')}")
            if 'topics' in row:
                click.echo(f"Topics: {', '.join(row.get('topics', []))}")
            click.echo("-" * 80)
        
        if output:
            # Use the enhanced export functionality
            export_df = api.prepare_dataframe_for_export(df)
            export_df.to_csv(output, index=False)
            click.echo(f"\nResults exported to {output} with the following columns:")
            click.echo(", ".join(export_df.columns))
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli()
