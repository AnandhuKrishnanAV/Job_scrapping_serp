#!/usr/bin/env python3
"""
Simple test script to validate SERP API key and connection
"""

import requests
import os
from dotenv import load_dotenv

def test_api_key():
    """Test if the SERP API key is working"""
    load_dotenv()
    
    api_key = os.getenv('SERP_API_KEY')
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    print(f"🔑 Testing API key: {api_key[:20]}...")
    
    # Simple test query
    params = {
        'engine': 'google',
        'q': 'test search',
        'api_key': api_key
    }
    
    try:
        response = requests.get('https://serpapi.com/search.json', params=params, timeout=10)
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API key is working!")
            print(f"📊 Search results found: {len(data.get('organic_results', []))}")
            return True
        elif response.status_code == 401:
            print("❌ Invalid API key - Please check your API key")
            return False
        elif response.status_code == 400:
            print("❌ Bad request - Check API parameters")
            print(f"Response: {response.text[:200]}")
            return False
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def test_google_jobs():
    """Test Google Jobs specifically"""
    load_dotenv()
    api_key = os.getenv('SERP_API_KEY')
    
    print("\n🔍 Testing Google Jobs API...")
    
    params = {
        'engine': 'google_jobs',
        'q': 'data analyst',
        'location': 'Berlin, Germany',
        'api_key': api_key,
        'hl': 'en',
        'gl': 'de'  # Use German locale
    }
    
    try:
        response = requests.get('https://serpapi.com/search.json', params=params, timeout=15)
        print(f"📡 Google Jobs response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs_results', [])
            print(f"✅ Found {len(jobs)} jobs!")
            
            if jobs:
                print("\n📋 Sample jobs:")
                for i, job in enumerate(jobs[:3], 1):
                    print(f"  {i}. {job.get('title', 'N/A')} at {job.get('company_name', 'N/A')}")
                    print(f"     📍 {job.get('location', 'N/A')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text[:300]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 SERP API Test Suite")
    print("=" * 40)
    
    # Test basic API
    if test_api_key():
        # Test Google Jobs
        test_google_jobs()
    else:
        print("\n💡 How to fix:")
        print("1. Go to https://serpapi.com/ and sign up")
        print("2. Get your API key from dashboard")
        print("3. Update .env file with: SERP_API_KEY=your_real_key")