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
    questions = []  # List to store the extracted questions and their details
    question_number = 1  # Counter for numbering the questions

    # Extract all <h3> headings which represent the questions
    for heading in frame_content.find_all('h3', class_='heading-element'):
        text = heading.get_text(strip=True)  # Extract and clean the text from the heading
        if text:
            classification = classify_question(text)  # Classify the question type
            
            # For each question, find associated answers (next <ul> element containing <li> items)
            answers_list = heading.find_next('ul')
            if answers_list:
                correct_answers = []
                incorrect_answers = []
                
                # Extract all task list items (answers)
                for item in answers_list.find_all('li', class_='task-list-item'):
                    checkbox = item.find('input', type='checkbox')
                    if checkbox and checkbox.get('checked'):
                        correct_answers.append(item.get_text(strip=True))  # Add correct answers
                    else:
                        incorrect_answers.append(item.get_text(strip=True))  # Add incorrect answers
                
                # Add question details to the list, with correct answers first
                questions.append([
                    f"{question_number}. {text}",
                    classification,
                    "; ".join(correct_answers),
                    "; ".join(incorrect_answers)
                ])

            question_number += 1  # Increment the question counter

    # Save the questions and answers to a CSV file
    with open('scraped_questions_and_answers.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Type', 'Correct Answers', 'Other Answers'])
        for question, classification, correct_answers, other_answers in questions:
            writer.writerow([question, classification, correct_answers, other_answers])

    print("Scraping completed and data saved to 'scraped_questions_and_answers.csv'.")

else:
    print("Content frame not found on the page.")
