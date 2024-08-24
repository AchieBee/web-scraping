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

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    URL = 'https://github.com/Ditectrev/AWS-Certified-Solutions-Architect-Associate-SAA-C03-Practice-Tests-Exams-Questions-Answers'
    driver.get(URL)

    wait = WebDriverWait(driver, 15)
    target_frame = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'turbo-frame#repo-content-turbo-frame')
    ))

    for _ in range(5):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    time.sleep(5)


    page_source = driver.page_source

finally:
    driver.quit()


soup = BeautifulSoup(page_source, 'html.parser')

frame_content = soup.find('turbo-frame', id='repo-content-turbo-frame')

def classify_question(text):
    lower_text = text.lower()
    if "choose 2 answers" in lower_text:
        return 'Multiple Answers (Checkbox)'
    if any(keyword in lower_text for keyword in ['list', 'select all', 'multiple']):
        return 'Multiple Answers'
    return 'Single Answer'

if frame_content:
    questions = []
    question_number = 1

    for heading in frame_content.find_all('h3', class_='heading-element'):
        text = heading.get_text(strip=True)
        if text:
            classification = classify_question(text)
            numbered_question = f"{question_number}. {text}"
            questions.append([numbered_question, classification])
            question_number += 1

    checked_items = []
    unchecked_items = []
    for item in frame_content.find_all('li', class_='task-list-item'):
        checkbox = item.find('input', type='checkbox')
        if checkbox and checkbox.get('checked'):
            checked_items.append(item.get_text(strip=True))
        else:
            unchecked_items.append(item.get_text(strip=True))

    checked_items.sort()
    sorted_task_list_items = checked_items + unchecked_items

    csv_filename_questions = 'questions.csv'
    with open(csv_filename_questions, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Numbered Heading', 'Type'])
        writer.writerows(questions)

    csv_filename_task_list = 'task_list_items.csv'
    with open(csv_filename_task_list, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Task List Item'])
        for item in sorted_task_list_items:
            writer.writerow([item])

    print(f"Extracted and classified {len(questions)} numbered headings and saved to '{csv_filename_questions}'.")
    print(f"Extracted {len(sorted_task_list_items)} task list items with checked items listed first and sorted in ascending order, and saved to '{csv_filename_task_list}'.")

else:
    print("Target <turbo-frame> not found.")
