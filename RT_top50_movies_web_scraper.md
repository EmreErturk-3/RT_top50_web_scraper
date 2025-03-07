# Rotten Tomatoes Top Movies Scraper

A Python-based web scraper that collects data about the top 50 movies from Rotten Tomatoes and analyzes the results.

## Usage

### Scraping Movies
```bash
python -m src.scraper
```

### Analyzing Results
```bash
python -m src.analyzer
```

## Features

- Scrapes the top 50 movies from Rotten Tomatoes
- Extracts movie rank, title, year, and score
- Performs decade-based analysis
- Generates visualizations:
  - Bar chart of movies by decade
  - Scatter plot of scores by decade
- Includes logging for error tracking and debugging

## Dependencies

- Beautiful Soup 4
- Requests
- Pandas
- Matplotlib
- and more (see requirements.txt)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
