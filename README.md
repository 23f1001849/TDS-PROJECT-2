# Data Analyst Agent

A powerful REST API that uses LLMs and data science tools to source, prepare, analyze, and visualize any data.

## Features

- **Web Scraping**: Automatically scrape data from websites like Wikipedia
- **Data Analysis**: Perform statistical analysis, correlations, and regression
- **Visualization**: Generate charts and plots as base64-encoded data URIs
- **Database Integration**: Query large datasets using DuckDB
- **LLM Integration**: Intelligent task parsing and analysis
- **RESTful API**: Simple POST endpoint for task submission

## Quick Start

### Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Server**
```bash
python main.py
```

The server will start on `http://localhost:8000`

3. **Test the API**
```bash
python test_agent.py
```

### Using Docker

1. **Build the Image**
```bash
docker build -t data-analyst-agent .
```

2. **Run the Container**
```bash
docker run -p 8000:8000 data-analyst-agent
```

## API Usage

### Endpoint
```
POST /api/
```

### Request Format
Send a POST request with a file containing the data analysis task description.

```bash
curl -X POST "http://localhost:8000/api/" -F "file=@question.txt"
```

### Response Format
The API returns results in JSON format, either as an array or object depending on the task.

## Supported Analysis Types

### 1. Wikipedia Data Analysis
Automatically scrapes Wikipedia tables and performs analysis:

```
Scrape the list of highest grossing films from Wikipedia...
1. How many $2 bn movies were released before 2020?
2. Which is the earliest film that grossed over $1.5 bn?
3. What's the correlation between the Rank and Peak?
4. Draw a scatterplot with regression line...
```

Response: `[1, "Titanic", 0.485782, "data:image/png;base64,..."]`

### 2. Database Analysis
Query large datasets using DuckDB:

```
The Indian high court judgement dataset...
{
  "Which high court disposed the most cases from 2019 - 2022?": "...",
  "What's the regression slope...": "...",
  "Plot the year and # of days of delay...": "data:image/webp;base64,..."
}
```

Response: JSON object with answers

## Architecture

### Core Components

- **FastAPI**: Web framework for the REST API
- **Pandas & NumPy**: Data manipulation and analysis
- **Matplotlib & Seaborn**: Data visualization
- **BeautifulSoup**: Web scraping
- **DuckDB**: Database queries and analytics
- **SciPy & Scikit-learn**: Statistical analysis and machine learning

### Data Processing Pipeline

1. **Task Parsing**: Parse incoming task descriptions
2. **Data Sourcing**: Scrape web data or query databases
3. **Data Processing**: Clean and prepare data for analysis
4. **Analysis**: Perform statistical analysis, correlations, regression
5. **Visualization**: Generate charts and encode as base64 data URIs
6. **Response**: Return results in requested format

## Configuration

### Environment Variables

- `PORT`: Server port (default: 8000)
- `OPENAI_API_KEY`: OpenAI API key for LLM features (optional)

### Data Sources

The agent can work with:
- Wikipedia tables
- S3 datasets (via DuckDB)
- CSV/JSON files
- Direct data input

## Deployment

### Cloud Deployment Options

1. **Heroku**
```bash
git init
heroku create your-app-name
git add .
git commit -m "Deploy data analyst agent"
git push heroku main
```

2. **AWS/GCP/Azure**
Use the provided Dockerfile to deploy on any container platform.

3. **Railway/Render**
Connect your GitHub repository for automatic deployment.

### Production Configuration

- Set appropriate memory limits for large datasets
- Configure timeout settings for long-running analysis
- Add authentication if needed
- Set up monitoring and logging

## Examples

### Example 1: Wikipedia Analysis
```python
import requests

with open('question.txt', 'rb') as f:
    response = requests.post('https://your-app.herokuapp.com/api/', files={'file': f})
    result = response.json()
    print(result)  # [1, "Titanic", 0.485782, "data:image/png;base64,..."]
```

### Example 2: Database Analysis
```python
import requests

with open('court_question.txt', 'rb') as f:
    response = requests.post('https://your-app.herokuapp.com/api/', files={'file': f})
    result = response.json()
    print(result)  # {"Which high court...": "33_10", ...}
```

## Testing

Run the test suite:
```bash
python test_agent.py
```

Check health:
```bash
curl http://localhost:8000/health
```

## Performance

- **Response Time**: < 3 minutes for most analyses
- **Image Size**: Plots optimized to < 100KB
- **Memory**: Efficient data processing with streaming where possible
- **Scalability**: Stateless design for horizontal scaling

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Timeout Errors**: Increase timeout for large datasets
3. **Memory Issues**: Use data streaming for large files
4. **Network Issues**: Check firewall settings and internet connectivity

### Debug Mode

Set environment variable for verbose logging:
```bash
export DEBUG=1
python main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
