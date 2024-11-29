# O'Reilly Bookfinder

A command-line tool to search and explore books from O'Reilly's learning platform. By default, it focuses on data science, AI, and machine learning content, but can search across all topics.

## Installation

This project uses Poetry for dependency management. To install:

```bash
# Clone the repository
git clone https://github.com/yourusername/oreilly-bookfinder.git
cd oreilly-bookfinder

# Install dependencies with Poetry
poetry install
```

## Usage

The tool provides a command-line interface with various search options. Here are some common use cases:

### Basic Search

```bash
# Search by query (defaults to data science/AI topics)
poetry run bookfinder search "machine learning"

# Search all topics
poetry run bookfinder search "python" --all-topics

# Limit number of results
poetry run bookfinder search "deep learning" --limit 5
```

### Author Search

```bash
# Search by author
poetry run bookfinder search --author "Joel Grus"

# Combine author and query search
poetry run bookfinder search "data science" --author "Joel Grus"
```

### Date Filtering

```bash
# Search for recent books
poetry run bookfinder search "python" --after 2023-01-01

# Search within a date range
poetry run bookfinder search "python" --after 2023-01-01 --before 2024-01-01

# Combine with other filters
poetry run bookfinder search "machine learning" --after 2023-01-01 --topic python
```

### Topic Filtering

```bash
# List available topics
poetry run bookfinder search --list-topics

# Search with specific topics
poetry run bookfinder search "python" --topic web-development --topic cloud

# Search all topics (disable default data science filter)
poetry run bookfinder search "python" --all-topics
```

### Pagination and Output

```bash
# Navigate through pages
poetry run bookfinder search "python" --page 1

# Save results to CSV
poetry run bookfinder search "machine learning" --output results.csv
```

## Features

- **Smart Defaults**: Automatically filters for data science, AI, and related topics
- **Author Search**: Find books by specific authors
- **Date Filtering**: Filter books by publication date
- **Topic Filtering**: Filter results by one or more topics
- **Flexible Search**: Combine query, author, date, and topic filters
- **CSV Export**: Save search results to CSV files
- **Pagination**: Navigate through multiple pages of results

## Command-Line Options

- `query`: Search query (optional if using --author)
- `--author, -a`: Search by author name
- `--after`: Only show books published after date (YYYY-MM-DD)
- `--before`: Only show books published before date (YYYY-MM-DD)
- `--limit, -l`: Number of results to return (default: 10)
- `--page, -p`: Page number for pagination (default: 0)
- `--output, -o`: Save results to CSV file
- `--topic, -t`: Filter by topic (can be used multiple times)
- `--list-topics`: Show available topics
- `--all-topics`: Search across all topics (disable default data science filter)

## Development

This project uses Poetry for dependency management. To set up for development:

```bash
# Install dev dependencies
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black .
```

## License

MIT License - see LICENSE file for details.