#!/usr/bin/env python3
"""
Daily Knowledge Bot

This script uses the Perplexity API to fetch an interesting fact about a rotating
topic each day. It can be scheduled to run daily using cron or Task Scheduler.

Usage:
  python daily_knowledge_bot.py

Requirements:
  - requests
"""

import requests
import json
import os
from datetime import datetime

# Store your API key securely (consider using environment variables in production)
# API_KEY = os.environ.get("PERPLEXITY_API_KEY")
API_KEY = "API_KEY"  # Replace with your actual API key


def get_daily_fact(topic):
    """
    Fetches an interesting fact about the given topic using Perplexity API.
    
    Args:
        topic (str): The topic to get a fact about
        
    Returns:
        str: An interesting fact about the topic
    """
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides interesting, accurate, and concise facts. Respond with only one fascinating fact, kept under 100 words."
            },
            {
                "role": "user",
                "content": f"Tell me an interesting fact about {topic} that most people don't know."
            }
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error making API request: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error parsing API response: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def save_fact_to_file(topic, fact):
    """
    Saves the fact to a text file with timestamp.
    
    Args:
        topic (str): The topic of the fact
        fact (str): The fact content
    """
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"daily_fact_{timestamp}.txt"
    
    with open(filename, "w") as f:
        f.write(f"DAILY FACT - {timestamp}\n")
        f.write(f"Topic: {topic}\n\n")
        f.write(fact)
    
    print(f"Fact saved to {filename}")


def main():
    """Main function that runs the daily knowledge bot."""
    # List of topics to rotate through
    # You could expand this to read from a configuration file
    topics = [
        "astronomy", 
        "history", 
        "biology", 
        "technology", 
        "psychology",
        "ocean life",
        "ancient civilizations",
        "quantum physics",
        "art history",
        "culinary science"
    ]
    
    # Use the current day of month to select a topic (rotates through the list)
    day = datetime.now().day
    topic_index = (day % len(topics)) - 1
    today_topic = topics[topic_index]
    
    print(f"Getting today's fact about: {today_topic}")
    
    # Get and display the fact
    fact = get_daily_fact(today_topic)
    print(f"\nToday's {today_topic} fact: {fact}")
    
    # Save the fact to a file
    save_fact_to_file(today_topic, fact)
    
    # In a real application, you might send this via email, SMS, etc.
    # Example: send_email("Daily Interesting Fact", fact, "your@email.com")


if __name__ == "__main__":
    main()
