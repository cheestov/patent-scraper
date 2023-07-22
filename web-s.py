import random
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from FCS import fcitations, scrapePatents

filename = "user-agent-list.txt"
lines = []
with open(filename, "r") as f:
   lines = f.readlines()
agent = random.choice(lines).strip()

#agent = random.choice(userAgents)  # this is used to get past the webscraping protections. I tell the browser im 1000 different users instead of 1
print(agent)
service = Service()
options = webdriver.ChromeOptions()
#options.add_argument("user-agent={}".format(agent))
#options.add_argument('--proxy-server=198.199.70.20:31028')
#options.add_argument('--proxy-server=154.65.39.7:80')
driver = webdriver.Chrome(service=service, options=options)  # object used to interact with chrome

driver.get("https://ppubs.uspto.gov/pubwebapp/external.html?q=2002.fy.") # search results for patents files in 2012

#switches to correct window in database
driver.maximize_window()
sleep(6)
chwd = driver.window_handles
driver.switch_to.window(chwd[1])
sleep(0.9)

pNumbers_states = scrapePatents(driver)

pNumbers = pNumbers_states[0]
states = pNumbers_states[1]

citations = fcitations(driver, pNumbers)
# removes duplicates due to inefficiant scrolling
#pNumbers = [*set(pNumbers)]

# pack it all into a csv using pandas
df = pd.DataFrame({'Patent #':pNumbers, 'Assignee State':states, 'Forward Citations':citations}) 
df.to_csv('products.csv', index=False, encoding='utf-8')


driver.quit()



