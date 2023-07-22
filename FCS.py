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

def scrapePatents(driver):
    pNumbers = []   # for storing patent numbers
    states = []     # for storing state info of patent
    #scrolls through results window and grabs the patent# from shown results
    # change number in while header to get more or less results.
    inner_window = driver.find_element(By.CLASS_NAME, "slick-viewport")
    scroll = 0
    while scroll < 30:  # this will scroll 3 times
        content = driver.page_source
        soup = BeautifulSoup(content)
        for a in soup.findAll('div', attrs={'class':'slick-cell l9 r9 left'}):
            pNumber=a.find('button', attrs={'class':'results-key-cntrl btn-link'})
            pNumbers.append(pNumber.text)
            print(pNumber.text)
            print(a['id'])
            driver.find_element(By.ID, a['id']).click()
            sleep(30)
            content2 = driver.page_source
            soup2 = BeautifulSoup(content2)
            state=soup2.find('div', attrs={'class':'item-row item-block meta-assigneeInfoGroup'})
            if state == None:
                states.append("N/A")
                continue
            state=state.findAll('div', attrs={'class':'item item-2 item-2-lg'})
            state=state[1].find('div', attrs={'class':'meta-col'})
            state = state.text
            print(state)
            states.append(state)
        for i in range(3):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', inner_window)
        scroll += 1
        sleep(.65)

    results = (pNumbers, states)
    return results