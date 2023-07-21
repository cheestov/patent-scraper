import random
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def scrapePatents(driver):
    pNumbers = []   # for storing patent numbers
    #scrolls through results window and grabs the patent# from shown results
    # change number in while header to get more or less results.
    inner_window = driver.find_element(By.CLASS_NAME, "slick-viewport")
    scroll = 0
    while scroll < 60:  # this will scroll 3 times
        content = driver.page_source
        soup = BeautifulSoup(content)
        for a in soup.findAll('div', attrs={'class':'slick-cell l9 r9 left'}):
            pNumber=a.find('button', attrs={'class':'results-key-cntrl btn-link'})
            pNumbers.append(pNumber.text)
            print(pNumber.text)
            print(a['id'])
            driver.find_element(By.ID, a['id']).click()
        for i in range(3):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', inner_window)
        scroll += 1
        sleep(.65)

    return pNumbers

filename = "user-agent-list.txt"
lines = []
with open(filename, "r") as f:
   lines = f.readlines()
agent = random.choice(lines).strip()

#agent = random.choice(userAgents)  # this is used to get past the webscraping protections. I tell the browser im 1000 different users instead of 1
print(agent)
service = Service()
options = webdriver.ChromeOptions()
options.add_argument("user-agent={}".format(agent))
#options.add_argument('--proxy-server=198.199.70.20:31028')
#options.add_argument('--proxy-server=154.65.39.7:80')
driver = webdriver.Chrome(service=service, options=options)  # object used to interact with chrome

driver.get("https://ppubs.uspto.gov/pubwebapp/external.html?q=2013.fy.") # search results for patents files in 2012

#switches to correct window in database
driver.maximize_window()
sleep(6)
chwd = driver.window_handles
driver.switch_to.window(chwd[1])
sleep(0.9)

pNumbers = scrapePatents(driver)


# removes duplicates due to inefficiant scrolling
pNumbers = [*set(pNumbers)]

# pack it all into a csv using pandas
df = pd.DataFrame({'Patent #':pNumbers}) 
df.to_csv('products.csv', index=False, encoding='utf-8')


driver.quit()



