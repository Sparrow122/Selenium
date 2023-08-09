from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
flag = True  
browser = webdriver.Chrome(options=option)

browser.get("https://github.com/TheDancerCodes")

def next_page(next_page_element):
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@alt='Avatar']")))
    except TimeoutException:
       print("Timed out waiting for page to load")
       browser.quit()
    
    next_page_element.click()
    time.sleep(5)
    parse_data()

def parse_data():
    global flag
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@alt='Avatar']")))
    except TimeoutException:
       print("Timed out waiting for page to load")
       browser.quit()
    time.sleep(7)
    language_element = browser.find_elements(By.CSS_SELECTOR,'li:has(span[itemprop="programmingLanguage"])')
    # use list comprehension to get the actual repo titles and not the selenium objects.
    list_of_json = []
    for i in language_element:
        list_of_json.append({"title": i.find_element(By.CSS_SELECTOR,"h3").text,
                             "lang": i.find_element(By.CSS_SELECTOR,'span[itemprop="programmingLanguage"]').text})
    print (list_of_json)
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='next_page']")))
    except TimeoutException:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='next_page disabled']")))
    try:
        no_next_page = browser.find_element('xpath',"//span[@class='next_page disabled']")
        if (no_next_page):
            print ("browser quit")
            browser.quit()
            flag = False
    except:
        print ("More pages are there")
    finally:
        if (flag):
            print ("next")
            next_page_element = browser.find_element("xpath","//a[@class='next_page']")
            next_page(next_page_element)
        else:
            print ("return")
            return


# Wait 20 seconds for page to load
timeout = 20
browser.find_element("xpath",'//nav[@aria-label="User profile"]//a[@data-tab-item="repositories"]').click()
WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@alt='Avatar']")))
parse_data()
if (flag):
    parse_data()
else:
    print ("done")

