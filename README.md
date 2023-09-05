# To-Do

### pre breakthrough notes
- [ ] set up the collection of more variables for each patent
    - Variables that can be collected:

    Patent number: _unique indentification number of each patent_
    
    Kind code: _https://www.uspto.gov/patents/search/authority-files/uspto-kind-codes#:~:text=B1-,B1,or%20after%20January%202%2C%202001. (Working through what all of these mean and what their relevence could be.)_
    
    CPC (A and I): _4 character code (Can include additional numbers identifying the subclass) that categorizes the invention e.g. 'fuel cell', 'metallurgic process'..._
    
    Assignee: _company filing, their state_
    
    publication date
    
    patent length/pages
    
    citations in patent
    
    ?Forward citations? : _not readily available. Could be difficult to collect in a reasonable time span as the web scraping for this takes a while_



    - [ ] feasability of collecting pdf or full text of the patent. 
    - [ ] figure out how to parse through there being multiple appointees, what does that mean for the patent?


- [ ] improve reliability of data collection
    - I did not get repeat data points but I am concerned about it skipping data points because it scrolls to far

    ** - [ ] test what patents are available during each scroll and then you can figure out how far to scroll and collect data  **
        - [ ] test scrolling to the bottom, how many are available? 

- [ ] Find new ways to get past web scraping blockers
    - collecting data from 2019 would take literal years with my current method of getting past web scraping blockers
- [ ] Properly document code. Make it more readable.
- [ ] Set up the program to work on the server and store data there

Optional
- [ ] CLI

--------------------------------------------------------------------------------------------------------------------------

Minutess I need to clock: 35 + 27


### Post break through notes
A complete break through. From further research ive realized ive taken a completely wrong appraoch, as one often does. 
https://ped.uspto.gov/peds/#/!/apiDoc
allows for the bulk downloading into a JSON. file size of all patents from 2019 = ~40GB from 7000 patents = ~350MB

I beleive this method does not include full patent text or forward citations. 

Questions:
- Data seems to download into multiple files of random size/number of patents in each. How to deal with this
- is it better to download the files through the api rather than the website, allowing this process to be done easily through the program
- Would it be better to process the data into some kind of database and then parse the data? Or would be better to parse the raw jsons. 
- 
