# Data Analyst Job Scraper

This Python script scrapes job listings for data analyst positions using the SERP API (SerpApi). It searches Google Jobs and saves the results in CSV and/or JSON format.

## Features

- 🔍 Search for data analyst jobs across multiple locations
- 📊 Detailed job analysis and statistics
- 💾 Export results to CSV and JSON formats
- 🔧 Environment variable configuration
- 📈 Company and location analytics
- ⚡ Rate limiting and error handling

## Setup

1. **Get a SERP API Key**
   - Go to [https://serpapi.com/](https://serpapi.com/)
   - Sign up for a free account
   - Get your API key from the dashboard

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your API key:
   ```
   SERP_API_KEY=your_actual_api_key_here
   ```

## Usage

### Basic Usage
```bash
python enhanced_job_scraper.py
```

### Using the Original Script
```bash
python job_scraper.py
```

### Programmatic Usage
```python
from enhanced_job_scraper import EnhancedJobScraper

# Initialize with API key
scraper = EnhancedJobScraper("your_api_key")

# Search for jobs
jobs = scraper.search_jobs(
    query="data analyst",
    location="New York, NY",
    num_results=100
)

# Analyze results
scraper.analyze_jobs()

# Save results
scraper.save_results("both")  # saves both CSV and JSON
```

## Configuration Options

You can configure the scraper using environment variables in your `.env` file:

```bash
# SERP API Configuration
SERP_API_KEY=your_api_key_here

# Job Search Configuration
DEFAULT_QUERY=data analyst
DEFAULT_LOCATION=United States
DEFAULT_NUM_RESULTS=50

# Output Configuration
OUTPUT_FORMAT=both  # csv, json, or both
```

## Output Files

The scraper generates timestamped files:
- `data_analyst_jobs_YYYYMMDD_HHMMSS.csv` - CSV format with job details
- `data_analyst_jobs_YYYYMMDD_HHMMSS.json` - JSON format with metadata

### CSV Fields
- title
- company
- location
- description
- salary
- url
- posted_date
- source

### JSON Structure
```json
{
  "total_jobs": 50,
  "scraped_at": "2025-10-26T...",
  "jobs": [
    {
      "title": "Data Analyst",
      "company": "Company Name",
      "location": "City, State",
      "description": "Job description...",
      "salary": "$60,000 - $80,000",
      "url": "https://...",
      "posted_date": "2 days ago",
      "source": "Google Jobs",
      "scraped_at": "2025-10-26T..."
    }
  ]
}
```

## Sample Analysis Output

```
📊 JOB ANALYSIS REPORT
==================================================
Total jobs found: 50

🏢 Top 10 Companies:
   1. Microsoft: 5 jobs
   2. Google: 4 jobs
   3. Amazon: 3 jobs
   ...

📍 Top 10 Locations:
   1. New York, NY: 8 jobs
   2. San Francisco, CA: 6 jobs
   3. Seattle, WA: 5 jobs
   ...

💰 Salary Information:
  Jobs with salary info: 35/50 (70.0%)
```

## Error Handling

The scraper includes comprehensive error handling for:
- Network timeouts and connection errors
- API rate limiting
- Invalid API keys
- Malformed response data
- File I/O errors

## API Limits

SerpApi free tier includes:
- 100 searches per month
- Rate limit: 1 request per second (built into the scraper)

## Troubleshooting

1. **"API key is required" error**
   - Check your `.env` file
   - Verify the API key is correct
   - Ensure no extra spaces

2. **"No jobs found" error**
   - Check your search query
   - Try different locations
   - Verify your API key is valid

3. **Rate limiting errors**
   - The scraper includes automatic rate limiting
   - Wait a few minutes between large searches

## License

This project is for educational and personal use only. Please respect the terms of service of job sites and APIs.