# patent-scraper

## Files to Browse


#### products.csv

This has the data collected. I ran it for a bit and got a sample of 270 patents from 2002. 
Very easy to read


#### web-s.py

This is the main file of the program. It uses selenium to set up chrome for the program, calls the webscraping functions, and uses pandas to compile the data into the csv


#### FCS.py

Has the two webscraping functions:

```def scrapePatents(driver):...```
this function scrolls and clicks through the results and gathers the patent # and state data

```def fCitations(driver, pIDs):...```
Uses the patent # collected to find out how many forward citations each patent has.