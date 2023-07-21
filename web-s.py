from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service


# basically scrape the the state id of the first assignee. N/A can be its own category I guess
# grab the amount of forward citations, so you would find the amount of results from an urpn search using that patents 
# patent number I think
# if that doesnt take too long, use py stata to make a chart?



service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
driver.get("https://www.amazon.com/s?k=laptops&crid=3SJI526XFJYQQ&sprefix=laptop%2Caps%2C109&ref=nb_sb_noss_1")

content = driver.page_source
soup = BeautifulSoup(content)
for a in soup.findAll('div', attrs={'class':'sg-col-inner'}):
    name=a.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'})
    products.append(name.text)
    price=a.find('span', attrs={'class':'a-price-whole'})
    prices.append(price.text)


df = pd.DataFrame({'Product Name':products, 'Product Price':prices}) 
df.to_csv('products.csv', index=False, encoding='utf-8')


driver.quit()