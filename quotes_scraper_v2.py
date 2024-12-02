from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

driver = webdriver.Chrome()
url = 'https://quotes.toscrape.com/login'
driver.get(url)

username_field = driver.find_element(By.NAME, 'username')
username_field.send_keys('Username')
password_field = driver.find_element(By.NAME, 'password')
password_field.send_keys('Password')
login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
login_button.click()
time.sleep(1)

data = []

for page in range(2):
    quotes = driver.find_elements(By.CLASS_NAME, 'quote')
    for quote in quotes:
        quote_text = quote.find_element(By.CLASS_NAME, 'text').text.replace('\u201c', '').replace('\u201d', '')
        author_name = quote.find_element(By.CLASS_NAME, 'author').text
        author_link = quote.find_element(By.CLASS_NAME, 'author').find_element(By.XPATH, '../a').get_attribute('href')
        tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, 'tag')]
        data.append({'author': author_name, 'quote': quote_text, 'author_link': author_link, 'tags': tags})
    if page == 0:
        next_button = driver.find_element(By.CLASS_NAME, 'next')
        next_button.find_element(By.TAG_NAME, 'a').click() 
        time.sleep(1)

output_file = 'quotes-v2.json'
with open(output_file, 'w') as json_file:
    json.dump(data, json_file, indent = 2)

driver.quit()