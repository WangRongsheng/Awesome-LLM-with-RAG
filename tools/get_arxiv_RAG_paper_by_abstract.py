import requests
from bs4 import BeautifulSoup
import re

# Define the URL
url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=%22Retrieval-Augmented%22&terms-0-field=abstract&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first"

# Fetch the content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the required information
papers = soup.find_all('li', class_='arxiv-result')
paper_details = []

for paper in papers:
    title = paper.find('p', class_='title is-5 mathjax').text.strip()
    link = paper.find('p', class_='list-title is-inline-block').find('a')['href']
    date = paper.find('p', class_='is-size-7').text.strip().split(';')[0].strip()
    
    # Extract date components using regex
    match = re.search(r"(\d{1,2}) ([A-Za-z]+), (\d{4})", date)
    day, month, year = match.groups()
    month_to_num = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
        'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }

    formatted_date = f"{year}.{month_to_num[month]}.{day.zfill(2)}"

    paper_details.append(f"- {title}. [*{formatted_date}*] [[Arxiv]({link})]")

# Save the details to a markdown file
with open('papers.md', 'w') as f:
    f.write('\n'.join(paper_details))

print("Scraping completed and saved to papers.md!")
