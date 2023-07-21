import random
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# basically scrape the the state id of the first assignee. N/A can be its own category I guess
# grab the amount of forward citations, so you would find the amount of results from an urpn search using that patents 
# patent number I think
# if that doesnt take too long, use py stata to make a chart?

pNumbers = []   # for storing patent numbers

filename = "user-agent-list.txt"
lines = []
with open(filename, "r") as f:
   lines = f.readlines()
agent = random.choice(lines).strip()

#agent = random.choice(userAgents)  # this is used to get past the webscraping protections. I tell the browser im 30 different users instead of 1
print(agent)
service = Service()
options = webdriver.ChromeOptions()
options.add_argument("user-agent={}".format(agent))
#options.add_argument('--proxy-server=198.199.70.20:31028')
driver = webdriver.Chrome(service=service, options=options)  # object used to interact with chrome

driver.get("https://ppubs.uspto.gov/pubwebapp/external.html?q=2013.fy.") # search results for patents files in 2012


sleep(6)
chwd = driver.window_handles
driver.switch_to.window(chwd[1])
sleep(0.9)




inner_window = driver.find_element(By.CLASS_NAME, "slick-viewport")
scroll = 0
while scroll < 20:  # this will scroll 3 times
    content = driver.page_source
    soup = BeautifulSoup(content)
    for a in soup.findAll('div', attrs={'class':'slick-cell l9 r9 left'}):
        pNumber=a.find('button', attrs={'class':'results-key-cntrl btn-link'})
        pNumbers.append(pNumber.text)
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', inner_window)
    scroll += 1
      # add appropriate wait here, of course. 1-2 seconds each
    sleep(1)

#content = driver.page_source
#soup = BeautifulSoup(content)
#for a in soup.findAll('div', attrs={'class':'slick-cell l9 r9 left'}):
#    pNumber=a.find('button', attrs={'class':'results-key-cntrl btn-link'})
 #   pNumbers.append(pNumber.text)
    
    


df = pd.DataFrame({'Patent #':pNumbers}) 
df.to_csv('products.csv', index=False, encoding='utf-8')


driver.quit()