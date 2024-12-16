import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Define the base URL for FOMC minutes
BASE_URL = "https://www.federalreserve.gov/monetarypolicy/files/"

# Wikipedia page with FOMC meeting dates
WIKI_URL = "https://en.wikipedia.org/wiki/History_of_Federal_Open_Market_Committee_actions"


def get_fomc_meeting_dates(wiki_url):
    """Scrape FOMC meeting dates from Wikipedia."""
    response = requests.get(wiki_url)
    if response.status_code != 200:
        print(f"Failed to fetch Wikipedia page, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    # Extract the meeting dates from the appropriate table
    # (Assuming the meeting dates are in a specific table on the page)
    tables = soup.find_all("table", {"class": "wikitable"})
    if not tables:
        print("No tables found on the page.")
        return []

    meeting_dates = []
    for table in tables:
        rows = table.find_all("tr")[1:]  # Skip the header row
        for row in rows:
            cells = row.find_all("td")
            if cells:
                date_text = cells[0].get_text(strip=True)
                try:
                    # Parse the date text into a datetime object
                    meeting_date = datetime.strptime(date_text, "%B %d, %Y")
                    meeting_dates.append(meeting_date)
                except ValueError:
                    continue  # Skip rows that do not have a valid date
    return meeting_dates


def generate_fomc_minutes_urls(meeting_dates):
    """Generate URLs for FOMC minutes based on meeting dates."""
    urls = []
    for date in meeting_dates:
        formatted_date = date.strftime("%Y%m%d")
        urls.append(f"{BASE_URL}fomcminutes{formatted_date}.pdf")
    return urls


def save_urls_to_file(urls, filename):
    """Save the generated URLs to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(urls))


# Fetch meeting dates from Wikipedia
meeting_dates = get_fomc_meeting_dates(WIKI_URL)

# Generate URLs for FOMC minutes
fomc_urls = generate_fomc_minutes_urls(meeting_dates)

# Save URLs to a file
save_urls_to_file(fomc_urls, "fomc_minutes_urls.txt")

print(f"Generated {len(fomc_urls)} FOMC minutes URLs and saved to 'fomc_minutes_urls.txt'.")
