"""Command line interface for O'Reilly Bookfinder."""
import click
from typing import List
from . import api

@click.group()
def cli():
    """Search and explore O'Reilly books."""
    pass

@cli.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Number of results to return')
@click.option('--page', '-p', default=0, help='Page number for pagination')
@click.option('--output', '-o', type=click.Path(), help='Save results to CSV file')
@click.option('--topic', '-t', multiple=True, help='Filter by topic (can be used multiple times)')
@click.option('--list-topics', is_flag=True, help='List available topics')
@click.option('--all-topics', is_flag=True, help='Search all topics (disable default data science filter)')
def search(query: str, limit: int, page: int, output: str, topic: List[str], list_topics: bool, all_topics: bool):
    """Search for books by title or topic. By default, searches only data science and AI topics."""
    if list_topics:
        topics = api.get_available_topics()
        click.echo("\nAvailable topics:")
        for t in topics:
            click.echo(f"- {t}")
        return
        
    try:
        df = api.search_books(
            query, 
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
            df.to_csv(output, index=False)
            click.echo(f"\nResults saved to {output}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli()
