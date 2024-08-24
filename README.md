
# Web Scraping with Selenium and BeautifulSoup

This project contains a Python script (web.py) that uses Selenium and BeautifulSoup to scrape content from a GitHub repository webpage. The script extracts questions (in the form of h3 headings) and corresponding answers (as list items with checkboxes) from the page. The extracted data is classified and saved into CSV files.
# Features

    Headless Browsing: The script uses a headless Chrome browser for scraping, meaning it runs without displaying a graphical interface.
    Question Classification: The script classifies each question as either requiring a single answer or multiple answers (checkboxes).
    Data Extraction: Extracted questions and answers are saved to questions.csv and task_list_items.csv respectively.

# Requirements

    Python 3.x
    pip for package management
    The following Python packages:
        selenium
        beautifulsoup4
        webdriver_manager

# Setup

    Create a Virtual Environment (Optional but Recommended):

    bash

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Required Packages:

Ensure you have the necessary Python packages installed:

bash

    pip install selenium beautifulsoup4 webdriver_manager

    Install ChromeDriver:

    The script uses webdriver_manager to automatically download and manage the correct version of ChromeDriver.

# Running the Script

    Execute the Script:

    Run the script using Python:

    bash

python web.py

# The script will perform the following actions:

    Navigate to the specified GitHub repository URL.
    Scroll down the page to ensure all content is loaded.
    Extract h3 headings (questions) and list items (answers) from the page.
    Classify and number the questions.
    Save the results to two CSV files: questions.csv and task_list_items.csv.

# Output Files:

After running the script, you will find the following files in the directory:

    questions.csv: Contains the extracted and classified questions, each numbered.
    task_list_items.csv: Contains the extracted task list items (answers), with checked items listed first.

This project is licensed under MIT License