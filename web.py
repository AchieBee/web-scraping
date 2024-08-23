import requests
from bs4 import BeautifulSoup
import json

# URL of the GitHub repository
url = 'https://github.com/Ditectrev/AWS-Certified-Solutions-Architect-Associate-SAA-C03-Practice-Tests-Exams-Questions-Answers'

# Payload for scraper API
payload = {
    'api_key': 'befc0eb3e75162db5167b8480375831e',
    'url': url,
    'render': 'true',
}

# Fetch the page
page = requests.get('https://api.scraperapi.com', params=payload)

# Parse the page with BeautifulSoup
soup = BeautifulSoup(page.text, 'html.parser')
repo = {}

try:
    # Extracting the repository name
    name_html_element = soup.find('strong', {"itemprop": "name"})
    repo['name'] = name_html_element.get_text().strip() if name_html_element else "N/A"

    # Extracting the latest commit datetime
    relative_time_html_element = soup.find('relative-time')
    repo['latest_commit'] = relative_time_html_element['datetime'] if relative_time_html_element else "N/A"

    # Extracting the branch name (with error handling)
    branch_element = soup.find('span', {"class": "Text-sc-17v1xeu-0 bOMzPg"})
    if branch_element:
        repo['branch'] = branch_element.get_text().strip()
    else:
        repo['branch'] = "N/A"
        print("Branch element not found, using 'N/A' as a fallback.")

    # Extracting the latest commit message
    commit_element = soup.find('span', {"class": "Text-sc-17v1xeu-0 gPDEWA fgColor-default"})
    repo['commit'] = commit_element.get_text().strip() if commit_element else "N/A"

    # Extracting the number of stars
    stars_element = soup.find('span', {"id": "repo-stars-counter-star"})
    repo['stars'] = stars_element.get_text().strip() if stars_element else "N/A"

    # Extracting the number of forks
    forks_element = soup.find('span', {"id": "repo-network-counter"})
    repo['forks'] = forks_element.get_text().strip() if forks_element else "N/A"

    # Extracting the repository description
    description_html_element = soup.find('p', {"class": "f4 my-3"})
    repo['description'] = description_html_element.get_text().strip() if description_html_element else "N/A"

    # Construct the README URL based on the extracted branch name
    main_branch = repo['branch'] if repo['branch'] != "N/A" else 'main'
    readme_url = f'https://raw.githubusercontent.com/Ditectrev/AWS-Certified-Solutions-Architect-Associate-SAA-C03-Practice-Tests-Exams-Questions-Answers/{main_branch}/README.md'
    
    # Fetch the README content
    readme_page = requests.get(readme_url)
    if readme_page.status_code != 404:
        repo['readme'] = readme_page.text
    else:
        repo['readme'] = "README not found"
    
    # Output the repository data
    print(repo)

    # Save the data to a JSON file
    with open('repo.json', 'w') as file:
        json.dump(repo, file, indent=4)
        print('Data saved to repo.json')

except Exception as e:
    print(f"An error occurred: {e}")
