import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define directory to store scraped articles
scraped_dir = "C:/Users/HP/OneDrive/Desktop/internship projects/scraped_articles"
os.makedirs(scraped_dir, exist_ok=True)  # Create directory if it doesn't exist

# Load URLs from Excel file
df = pd.read_excel("input.xlsx")  # Ensure "input.xlsx" exists in the correct location

def scrape_article(url):
    """Extracts the article title and content from the given URL."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title (h1 with class 'entry-title')
        title = soup.find("h1", class_="entry-title")
        title = title.get_text(strip=True) if title else "No Title Found"

        # Extract content (all p tags inside div with class 'td-ss-main-content')
        content_div = soup.find("div", class_="td-ss-main-content")
        paragraphs = content_div.find_all("p") if content_div else []
        content = "\n".join(p.text.strip() for p in paragraphs)

        return title, content

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None, None

# Loop through each URL in the Excel file
for index, row in df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]
    
    title, content = scrape_article(url)

    if title and content:
        # Save the scraped article in the scraped_articles directory
        file_path = os.path.join(scraped_dir, f"{url_id}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"Title: {title}\n\n{content}")

        print(f"Scraped and saved: {file_path}")
