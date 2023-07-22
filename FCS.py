from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def fcitations(driver, pIDs) :
    pNumbers = []
    fCitations = []
    for i in pIDs:
        pNumbers.append(str(i)[3:len(str(i)) - 3])
    
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div[3]/div[1]/div[2]/div/div/div/div[1]/div[3]/div/button").click()
    sleep(1)

    for i in pNumbers :
        sBar = driver.find_element(By.CLASS_NAME, "trix")
        sBar.clear()
        sleep(1)
        sBar.send_keys("{}.urpn.".format(i))
        sBar.send_keys(Keys.RETURN)
        sleep(3)

        content = driver.page_source
        soup = BeautifulSoup(content)

        result = soup.find('div', attrs={'class':'resultNumber'})
        result = result.text
        print(result)

        fCitations.append(result)
        sleep(30)
    
    return fCitations

