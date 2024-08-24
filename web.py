import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Configure Selenium WebDriver options for Chrome (headless mode)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver using the webdriver-manager for automatic driver installation
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Specify the URL of the webpage to scrape
    URL = 'https://github.com/Ditectrev/AWS-Certified-Solutions-Architect-Associate-SAA-C03-Practice-Tests-Exams-Questions-Answers'
    driver.get(URL)  # Open the URL in the browser

    # Wait for the <turbo-frame> containing the main content to load
    wait = WebDriverWait(driver, 15)
    target_frame = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'turbo-frame#repo-content-turbo-frame')
    ))

    # Scroll down the page to potentially load more dynamic content
    for _ in range(5):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(2)  # Pause to allow content to load

    # Additional pause to ensure all dynamic content has loaded
    time.sleep(5)

    # Capture the full page source after the dynamic content has loaded
    page_source = driver.page_source

finally:
    # Close the WebDriver (browser) after the operation is complete
    driver.quit()

# Parse the captured page source using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find the specific <turbo-frame> that contains the content we want to scrape
frame_content = soup.find('turbo-frame', id='repo-content-turbo-frame')

# Function to classify the type of question based on its text
def classify_question(text):
    lower_text = text.lower()

    if "choose 2 answers" in lower_text:
        return 'Multiple Answers (Checkbox)'  # Identifies questions requiring multiple answers
    if any(keyword in lower_text for keyword in ['list', 'select all', 'multiple']):
        return 'Multiple Answers'  # Identifies other types of multiple-answer questions
    return 'Single Answer'  # Default classification for single-answer questions

if frame_content:
    questions = []  # List to store the extracted questions
    question_number = 1  # Counter for numbering the questions

    # Extract all <h3> headings which represent the questions
    for heading in frame_content.find_all('h3', class_='heading-element'):
        text = heading.get_text(strip=True)  # Extract and clean the text from the heading
        if text:
            classification = classify_question(text)  # Classify the question type
            numbered_question = f"{question_number}. {text}"  # Number the question
            questions.append([numbered_question, classification])  # Add to the list
            question_number += 1  # Increment the question counter

    checked_items = []  # List to store checked (correct) items
    unchecked_items = []  # List to store unchecked items

    # Extract all task list items (answers)
    for item in frame_content.find_all('li', class_='task-list-item'):
        checkbox = item.find('input', type='checkbox')
        if checkbox and checkbox.get('checked'):
            checked_items.append(item.get_text(strip=True))  # Add checked items to the list
        else:
            unchecked_items.append(item.get_text(strip=True))  # Add unchecked items to the list

    # Sort the checked items and combine with unchecked items
    checked_items.sort()
    sorted_task_list_items = checked_items + unchecked_items

    # Save the extracted and classified questions to a CSV file
    csv_filename_questions = 'questions.csv'
    with open(csv_filename_questions, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Numbered Heading', 'Type'])  # Header row
        writer.writerows(questions)  # Write the questions data

    # Save the extracted task list items (answers) to a CSV file
    csv_filename_task_list = 'task_list_items.csv'
    with open(csv_filename_task_list, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Task List Item'])  # Header row
        for item in sorted_task_list_items:
            writer.writerow([item])  # Write each item to the file

    print(f"Extracted and classified {len(questions)} numbered headings and saved to '{csv_filename_questions}'.")
    print(f"Extracted {len(sorted_task_list_items)} task list items with checked items listed first and sorted in ascending order, and saved to '{csv_filename_task_list}'.")

else:
    # Print a message if the target content could not be found
    print("Target <turbo-frame> not found.")
