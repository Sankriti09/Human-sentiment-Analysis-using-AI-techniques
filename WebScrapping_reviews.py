import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sqlite3 as sql

urls = []
product_urls = []
list_of_reviews = []

#each page urls 
for i in range(1,252):
    urls.append(f"https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&explicit=1&page={i}")

#scraping each product's urls |16,064 products
for url in urls:
    try:
        driver = webdriver.Chrome(executable_path = r"C:\Users\dell\UI webpage\chromedriver_win32\chromedriver.exe")
        driver.get(url)
        sleep(5)
        for i in range(1,65):
            product = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[1]/div/div/ul/li[{i}]/div/a')))
            product_urls.append(product.get_attribute('href'))
    except TimeoutException:
        pass
        
#scraping each product's reviews
driver = webdriver.Chrome(executable_path = r"C:\Users\dell\UI webpage\chromedriver_win32\chromedriver.exe")
for product_url in product_urls[15:]:
    try:
        driver.get(product_url)
        sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html,'html')
        for i in range(4):
            try:
                list_of_reviews.append(soup.select(f'#review-preview-toggle-{i}')[0].getText().strip())
            except:
                continue
        while(True):
            try:
                next_button = driver.find_element('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a[contains(@href, "https")]')
                if next_button!= None:
                    next_button.click()
                    sleep(5)
                    html = driver.page_source
                    soup = BeautifulSoup(html,'html')
                    for i in range(4):
                        try:
                            list_of_reviews.append(soup.select(f'#review-preview-toggle-{i}')[0].getText().strip())
                        except:
                            continue
            except Exception as e:
                print("FINISH : ",e)
                break
    except:
        continue
    
scrapedallreviews = pd.DataFrame(list_of_reviews, index = None, columns = ['reviews'])
scrapedallreviews.to_csv("scrappedReviews.csv")

df = pd.read_csv("scrappedReviews.csv")
conn = sql.connect("scrappedReviews.db")
df.to_sql('scrapedreviewstable', conn)
