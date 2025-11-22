#!/usr/bin/env python3
"""
German job scraper for data science students
Searches for multiple relevant job types and appends to master files
"""

import requests
import json
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Master file names
MASTER_CSV_FILE = "data_science_jobs_master.csv"
MASTER_HTML_FILE = "data_science_jobs_master.html"

def get_data_science_job_queries():
    """Return job queries relevant for data science students"""
    return {
        "Data Analyst": "data analyst",
        "Business Analyst": "business analyst", 
        "Data Scientist": "data scientist",
        "Business Intelligence Analyst": "business intelligence analyst",
        "Junior Data Analyst": "junior data analyst",
        "Entry Level Data Analyst": "entry level data analyst",
        "Data Science Intern": "data science intern",
        "Business Intelligence Developer": "business intelligence developer",
        "Market Research Analyst": "market research analyst",
        "Operations Analyst": "operations analyst",
        "Financial Analyst": "financial analyst",
        "Product Analyst": "product analyst",
        "Marketing Analyst": "marketing analyst",
        "Research Analyst": "research analyst",
        "Quantitative Analyst": "quantitative analyst"
    }

def search_german_jobs_multiple_types():
    """Search for multiple job types relevant to data science students"""
    
    api_key = os.getenv('SERP_API_KEY')
    german_cities = [
        "Berlin, Germany",
        "Munich, Germany", 
        "Hamburg, Germany",
        "Frankfurt, Germany",
        "Cologne, Germany",
        "Stuttgart, Germany",
        "Düsseldorf, Germany"
    ]
    
    job_queries = get_data_science_job_queries()
    all_jobs = []
    
    print(f"🎯 Searching for {len(job_queries)} different job types...")
    print(f"📍 Across {len(german_cities)} German cities...")
    
    for job_type, query in job_queries.items():
        print(f"\n🔍 Searching for: {job_type}")
        
        for city in german_cities:
            print(f"   📍 In {city}...")
            
            params = {
                'engine': 'google_jobs',
                'q': query,
                'location': city,
                'api_key': api_key,
                'hl': 'en',
                'gl': 'de'
            }
            
            try:
                response = requests.get('https://serpapi.com/search.json', params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('jobs_results', [])
                    
                    if jobs:
                        print(f"      ✅ Found {len(jobs)} jobs")
                        
                        # Take top 2 jobs per city per query to avoid too many results
                        for job in jobs[:2]:
                            # Get application URL
                            apply_url = (
                                job.get('apply_link') or 
                                job.get('link') or 
                                (job.get('apply_options', [{}])[0].get('link') if job.get('apply_options') else None) or
                                'No direct link available'
                            )
                            
                            # Extract salary info
                            salary = 'Not specified'
                            if 'detected_extensions' in job and job['detected_extensions']:
                                extensions = job['detected_extensions']
                                if 'salary' in extensions:
                                    salary = extensions['salary']
                            
                            # Extract posted date
                            posted_date = 'Not specified'
                            if 'detected_extensions' in job and job['detected_extensions']:
                                extensions = job['detected_extensions']
                                if 'posted_at' in extensions:
                                    posted_date = extensions['posted_at']
                            
                            job_data = {
                                'title': job.get('title', 'N/A'),
                                'company': job.get('company_name', 'N/A'),
                                'location': job.get('location', city),
                                'description': job.get('description', 'N/A')[:300] + '...' if len(job.get('description', '')) > 300 else job.get('description', 'N/A'),
                                'salary': salary,
                                'apply_url': apply_url,
                                'posted_date': posted_date,
                                'source': 'Google Jobs',
                                'job_id': job.get('job_id', 'N/A'),
                                'search_city': city,
                                'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'search_query': query,
                                'job_category': job_type
                            }
                            
                            all_jobs.append(job_data)
                    else:
                        print(f"      ➖ No jobs found")
                        
                else:
                    print(f"      ❌ Error: {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ Error: {e}")
    
    return all_jobs

def load_existing_jobs():
    """Load existing jobs from master CSV file to avoid duplicates"""
    existing_jobs = set()
    
    if os.path.exists(MASTER_CSV_FILE):
        try:
            with open(MASTER_CSV_FILE, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Create a unique identifier for each job
                    job_signature = f"{row.get('title', '')}-{row.get('company', '')}-{row.get('location', '')}"
                    existing_jobs.add(job_signature)
        except Exception as e:
            print(f"⚠️  Could not load existing jobs: {e}")
    
    return existing_jobs

def append_jobs_to_master_files(new_jobs):
    """Append new jobs to master CSV and HTML files"""
    if not new_jobs:
        print("No new jobs to add.")
        return 0
    
    # Load existing jobs to avoid duplicates
    existing_jobs = load_existing_jobs()
    
    # Filter out duplicate jobs
    unique_jobs = []
    duplicates = 0
    
    for job in new_jobs:
        job_signature = f"{job['title']}-{job['company']}-{job['location']}"
        if job_signature not in existing_jobs:
            unique_jobs.append(job)
            existing_jobs.add(job_signature)
        else:
            duplicates += 1
    
    if duplicates > 0:
        print(f"🔄 Skipped {duplicates} duplicate jobs")
    
    if not unique_jobs:
        print("ℹ️  No new unique jobs to add.")
        return 0
    
    # Check if CSV file exists to determine if we need headers
    file_exists = os.path.exists(MASTER_CSV_FILE)
    
    # Append to CSV file
    with open(MASTER_CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'company', 'location', 'description', 'salary', 'apply_url', 'posted_date', 'source', 'job_id', 'search_city', 'scraped_at', 'search_query', 'job_category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if file is new
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(unique_jobs)
    
    print(f"✅ Added {len(unique_jobs)} new jobs to {MASTER_CSV_FILE}")
    
    # Update HTML file with all jobs
    update_master_html_file()
    
    return len(unique_jobs)

def update_master_html_file():
    """Recreate the master HTML file with all jobs, organized by category"""
    try:
        # Read all jobs from CSV
        all_jobs = []
        with open(MASTER_CSV_FILE, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            all_jobs = list(reader)
        
        # Sort by category, then by scraped date (newest first)
        all_jobs.sort(key=lambda x: (x.get('job_category', 'Unknown'), x.get('scraped_at', '')), reverse=True)
        
        # Group jobs by category
        jobs_by_category = {}
        for job in all_jobs:
            category = job.get('job_category', 'Other')
            if category not in jobs_by_category:
                jobs_by_category[category] = []
            jobs_by_category[category].append(job)
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Science Jobs Database - Germany</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; }}
                h1 {{ color: #2c3e50; text-align: center; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                .stats {{ text-align: center; margin: 20px 0; padding: 20px; background-color: #ecf0f1; border-radius: 5px; }}
                .category-stats {{ display: flex; justify-content: space-around; flex-wrap: wrap; margin: 20px 0; }}
                .category-stat {{ background-color: #3498db; color: white; padding: 10px; margin: 5px; border-radius: 5px; text-align: center; }}
                .job-card {{ border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; background-color: #fafafa; }}
                .job-title {{ color: #2980b9; font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }}
                .company {{ color: #27ae60; font-weight: bold; margin-bottom: 5px; }}
                .location {{ color: #7f8c8d; margin-bottom: 10px; }}
                .salary {{ color: #e74c3c; font-weight: bold; margin-bottom: 10px; }}
                .description {{ margin: 10px 0; line-height: 1.4; }}
                .apply-btn {{ 
                    display: inline-block; 
                    background-color: #3498db; 
                    color: white; 
                    padding: 10px 20px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin-top: 10px; 
                    font-weight: bold;
                }}
                .apply-btn:hover {{ background-color: #2980b9; }}
                .job-meta {{ display: flex; justify-content: space-between; align-items: center; margin-top: 15px; }}
                .scraped-info {{ color: #95a5a6; font-size: 0.8em; }}
                .category-badge {{ background-color: #9b59b6; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎓 Data Science Jobs Database - Germany</h1>
                <div class="stats">
                    <strong>Total Jobs: {len(all_jobs)}</strong> | 
                    <strong>Job Categories: {len(jobs_by_category)}</strong> | 
                    <strong>Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</strong>
                </div>
                
                <div class="category-stats">
        """
        
        # Add category statistics
        for category, jobs in jobs_by_category.items():
            html_content += f'<div class="category-stat">{category}<br><strong>{len(jobs)} jobs</strong></div>'
        
        html_content += '</div>'
        
        # Add jobs by category
        for category, jobs in jobs_by_category.items():
            html_content += f'<h2>📊 {category} ({len(jobs)} jobs)</h2>'
            
            for i, job in enumerate(jobs, 1):
                apply_link = job.get('apply_url', '')
                if apply_link and apply_link != "No direct link available" and apply_link.startswith('http'):
                    apply_button = f'<a href="{apply_link}" target="_blank" class="apply-btn">🚀 Apply Now</a>'
                else:
                    apply_button = f'<span style="color: #e74c3c;">🔍 Search manually on Google Jobs</span>'
                
                salary_display = f'<div class="salary">💰 {job.get("salary", "Not specified")}</div>' if job.get("salary") != "Not specified" else ""
                
                html_content += f"""
                    <div class="job-card">
                        <div class="job-title">{job.get('title', 'N/A')} <span class="category-badge">{category}</span></div>
                        <div class="company">🏢 {job.get('company', 'N/A')}</div>
                        <div class="location">📍 {job.get('location', 'N/A')}</div>
                        {salary_display}
                        <div class="description">{job.get('description', 'N/A')}</div>
                        <div class="job-meta">
                            {apply_button}
                            <div class="scraped-info">
                                📅 Posted: {job.get('posted_date', 'Not specified')}<br>
                                🕒 Found: {job.get('scraped_at', 'Unknown')}
                            </div>
                        </div>
                    </div>
                """
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        # Write HTML file
        with open(MASTER_HTML_FILE, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)
        
        print(f"✅ Updated {MASTER_HTML_FILE} with all {len(all_jobs)} jobs organized by category")
        
    except Exception as e:
        print(f"❌ Error updating HTML file: {e}")

def show_master_file_stats():
    """Show statistics about the master file"""
    if not os.path.exists(MASTER_CSV_FILE):
        print("📊 No master database exists yet.")
        return
    
    try:
        with open(MASTER_CSV_FILE, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            jobs = list(reader)
        
        print(f"\n📊 DATA SCIENCE JOBS DATABASE STATS:")
        print(f"   Total jobs: {len(jobs)}")
        
        if jobs:
            # Category stats
            categories = {}
            companies = {}
            cities = {}
            
            for job in jobs:
                category = job.get('job_category', 'Unknown')
                company = job.get('company', 'Unknown')
                city = job.get('search_city', 'Unknown')
                
                categories[category] = categories.get(category, 0) + 1
                companies[company] = companies.get(company, 0) + 1
                cities[city] = cities.get(city, 0) + 1
            
            print(f"   Job categories: {len(categories)}")
            print(f"   Top categories:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"      • {category}: {count} jobs")
            
            print(f"   Unique companies: {len(companies)}")
            print(f"   Cities with jobs: {len(cities)}")
            
            # Show date range
            dates = [job.get('scraped_at') for job in jobs if job.get('scraped_at')]
            if dates:
                dates.sort()
                print(f"   Data from: {dates[0]} to {dates[-1]}")
    
    except Exception as e:
        print(f"❌ Error reading master file: {e}")

def main():
    print("🎓 Data Science Student Job Scraper - Germany")
    print("=" * 55)
    print("🎯 Searching for jobs suitable for data science students:")
    
    job_queries = get_data_science_job_queries()
    for i, (job_type, query) in enumerate(job_queries.items(), 1):
        print(f"   {i:2d}. {job_type}")
    
    # Show current stats
    show_master_file_stats()
    
    confirm = input(f"\nSearch for all {len(job_queries)} job types? (y/n): ").strip().lower()
    
    if confirm == 'y':
        # Search for jobs
        print(f"\n🔍 Starting comprehensive job search...")
        new_jobs = search_german_jobs_multiple_types()
        
        if new_jobs:
            print(f"\n📊 SEARCH RESULTS")
            print(f"Found {len(new_jobs)} total jobs across all categories")
            
            # Add to master files
            added_count = append_jobs_to_master_files(new_jobs)
            
            if added_count > 0:
                print(f"\n📁 MASTER FILES UPDATED:")
                print(f"   📊 CSV: {MASTER_CSV_FILE}")
                print(f"   🌐 HTML: {MASTER_HTML_FILE}")
                print(f"\n💡 Open {MASTER_HTML_FILE} in your browser to see all jobs organized by category!")
            
            # Show updated stats
            show_master_file_stats()
            
        else:
            print("❌ No jobs found in this search.")
    else:
        print("Search cancelled.")

if __name__ == "__main__":
    main()