from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


# Set up Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (without GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options=chrome_options)

# Load the URL
print("Getting URL...")
driver.get("https://www.firs.gov.ng/tax-resources-statistics")

time.sleep(8)  # It's better to use WebDriverWait, but for simplicity, we use sleep here

# Locate the table rows (excluding header)
print("Getting rows..")

try:
    rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'min-w-max')]//tbody/tr")

    print(rows)

    # Loop through each row and extract text
    data = []
    for row in rows:
        print("Loop execution start..")
        columns = row.find_elements(By.TAG_NAME, "td")  # Find all td elements (data cells) in the row
        row_data = [col.text.strip() for col in columns]  # Extract the text from each column
        data.append(row_data)

    for row in data:
        print(row)

except Exception as e:
    print(f"Whoops: {e}")



driver.quit()