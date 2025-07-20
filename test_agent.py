#!/usr/bin/env python3
"""
Test script for the Data Analyst Agent
"""

import requests
import json

def test_wikipedia_analysis():
    """Test Wikipedia films analysis"""
    
    question = """
Scrape the list of highest grossing films from Wikipedia. It is at the URL:
https://en.wikipedia.org/wiki/List_of_highest-grossing_films

Answer the following questions and respond with a JSON array of strings containing the answer.

1. How many $2 bn movies were released before 2020?
2. Which is the earliest film that grossed over $1.5 bn?
3. What's the correlation between the Rank and Peak?
4. Draw a scatterplot of Rank and Peak along with a dotted red regression line through it.
   Return as a base-64 encoded data URI, `"data:image/png;base64,iVBORw0KG..."` under 100,000 bytes.
"""
    
    # Save question to file
    with open('question.txt', 'w') as f:
        f.write(question)
    
    # Test the API
    url = "http://localhost:8000/api/"
    
    try:
        with open('question.txt', 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            print("Wikipedia Analysis Result:")
            print(json.dumps(result, indent=2))
            return result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error testing API: {e}")
        return None

def test_court_analysis():
    """Test Indian High Court analysis"""
    
    question = """
The Indian high court judgement dataset contains judgements from the Indian High Courts, downloaded from [ecourts website](https://judgments.ecourts.gov.in/). It contains judgments of 25 high courts, along with raw metadata (as .json) and structured metadata (as .parquet).

- 25 high courts
- ~16M judgments
- ~1TB of data

Structure of the data in the bucket:

- `data/pdf/year=2025/court=xyz/bench=xyz/judgment1.pdf,judgment2.pdf`
- `metadata/json/year=2025/court=xyz/bench=xyz/judgment1.json,judgment2.json`
- `metadata/parquet/year=2025/court=xyz/bench=xyz/metadata.parquet`
- `metadata/tar/year=2025/court=xyz/bench=xyz/metadata.tar.gz`
- `data/tar/year=2025/court=xyz/bench=xyz/pdfs.tar`

This DuckDB query counts the number of decisions in the dataset.

```sql
INSTALL httpfs; LOAD httpfs;
INSTALL parquet; LOAD parquet;

SELECT COUNT(*) FROM read_parquet('s3://indian-high-court-judgments/metadata/parquet/year=*/court=*/bench=*/metadata.parquet?s3_region=ap-south-1');
```

Here are the columns in the data:

| Column                 | Type    | Description                    |
| ---------------------- | ------- | ------------------------------ |
| `court_code`           | VARCHAR | Court identifier (e.g., 33~10) |
| `title`                | VARCHAR | Case title and parties         |
| `description`          | VARCHAR | Case description               |
| `judge`                | VARCHAR | Presiding judge(s)             |
| `pdf_link`             | VARCHAR | Link to judgment PDF           |
| `cnr`                  | VARCHAR | Case Number Register           |
| `date_of_registration` | VARCHAR | Registration date              |
| `decision_date`        | DATE    | Date of judgment               |
| `disposal_nature`      | VARCHAR | Case outcome                   |
| `court`                | VARCHAR | Court name                     |
| `raw_html`             | VARCHAR | Original HTML content          |
| `bench`                | VARCHAR | Bench identifier               |
| `year`                 | BIGINT  | Year partition                 |

Answer the following questions and respond with a JSON object containing the answer.

{
  "Which high court disposed the most cases from 2019 - 2022?": "...",
  "What's the regression slope of the date_of_registration - decision_date by year in the court=33_10?": "...",
  "Plot the year and # of days of delay from the above question as a scatterplot with a regression line. Encode as a base64 data URI under 100,000 characters": "data:image/webp:base64,..."
}
"""
    
    # Save question to file
    with open('court_question.txt', 'w') as f:
        f.write(question)
    
    # Test the API
    url = "http://localhost:8000/api/"
    
    try:
        with open('court_question.txt', 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            print("Court Analysis Result:")
            print(json.dumps(result, indent=2))
            return result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error testing API: {e}")
        return None

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("Health Check:", response.json())
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Health check error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Data Analyst Agent...")
    
    # Test health check first
    if test_health_check():
        print("\n" + "="*50)
        
        # Test Wikipedia analysis
        print("Testing Wikipedia Analysis...")
        wiki_result = test_wikipedia_analysis()
        
        print("\n" + "="*50)
        
        # Test Court analysis
        print("Testing Court Analysis...")
        court_result = test_court_analysis()
        
        print("\n" + "="*50)
        print("Testing completed!")
    else:
        print("Server is not running. Please start the server first with: python main.py")
