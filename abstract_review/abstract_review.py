from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
product_name = input("Enter product name: ").strip().replace(" ", "_")
product_url = input("Enter Flipkart product URL: ")

# sir Start Chrome browser where the driver helps and manages the browser and the webdriver_manager helps to install the driver automatically

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window() # sir it Maximize window for better visibility

# Open Flipkart product page
driver.get(product_url)
wait = WebDriverWait(driver, 10) # sir wait for driver 10 seconds to load the page

# finding view all and Click on "View All" reviews bcz as not all reviews are visible on the page
try:
    view_all_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "_23J90q"))) #here fetching class bcz 'All 40745 reviews' which is change over time
    view_all_button.click()
    
except:
    print("Couldn't find 'View All' button!")

review_list = []

# Start scraping
while True:
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ZmyHeo"))) # wait for reviews to load
        reviews = driver.find_elements(By.CLASS_NAME, "ZmyHeo") 
        
        for review in reviews:
            review_text = review.text.strip() # Extract review text and clean while removing the spaces and other unwanted characters
            if review_text:
                review_list.append(review_text)
                print(review_text)

        # Click on 'Next' if available
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(2) 

    except Exception as e:
        print("No more pages left. Scraping complete!")
        break

# Save into CSV
file_name = f"{product_name}_reviews.csv"
with open(file_name, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Review"])
    for r in review_list:
        writer.writerow([r])

print(f"✅ All {len(review_list)} reviews saved into {file_name} successfully!")

driver.quit()
