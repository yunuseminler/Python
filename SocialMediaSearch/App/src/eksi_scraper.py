import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import csv
from selenium import webdriver
import time
i = 0
def search(ilac):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(executable_path="chromedriver.exe",options=chrome_options)

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277" # random user agent

     #initialize colorama for windows

    args = "https://eksisozluk.com/"+ilac # parse all arguments
    output = "./doc/EK"+ilac +".csv"
    async def fetch(session, url, writer):
        async with session.get(url, headers={'User-Agent':USER_AGENT}) as resp: 
            text_resp = await resp.text() # source of page
            soup = BeautifulSoup(text_resp, 'html.parser') # convert string to soup object
            entry = soup.find('div', {'class':'content'}) # find entry content
            entry_date = soup.find('a', {'class':'entry-date permalink'}) # find date of the entry
            entry_author = soup.find('a', {'class':'entry-author'}) # find author of the entry
            while entry is not None: # iterate until entry object not None 
                data = {
                    'Entry': entry.text.replace('\n','').replace('\r', '').replace('\t', '').replace('    ', ''), # clear the contents of the entry from unnecessary things
                    'Date': entry_date.text,
                    'Author': entry_author.text
                }
                output_entry(writer, output, data) # print message and write entry to file
                entry = entry.find_next('div', {'class':'content'}) # find next entry content
                entry_date = entry_date.find_next('a', {'class':'entry-date permalink'}) # find next date of the entry
                entry_author = entry_author.find_next('a', {'class':'entry-author'}) # find next author of the entry

    async def main(args, last_page, writer):
        async with aiohttp.ClientSession() as session: # start request session for speed up
            tasks = [fetch(session, f'{args}?p={i}', writer) for i in range(1, last_page + 1)] # create tasks
            await asyncio.gather(*tasks) # wait coroutines until they complete

    def page_counts(url):
        """
            Get page counts of the titles
        """
        r = requests.get(url, headers={'User-Agent':USER_AGENT})
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            last_page = soup.find('div', {'class':'pager'})['data-pagecount']
        except TypeError:
            last_page = 1
        return int(last_page)

    
    def output_entry(writer, output_file, data):
        """
            Prints entry data and then write it to csv file.
        """
        global i
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f'[{dt_string}] '+ 'INFO ' + f'{data}')
        i += 1
        writer.writerow([data['Entry'], data['Date'], data['Author']])


    fp = open(output, 'w', encoding='UTF-8', newline='')
    writer = csv.writer(fp) # create csv writer
    writer.writerow(['Entry', 'Date', 'Author']) # write csv column names
    driver.get(args)
    args = driver.current_url
    last_page = page_counts(args) # get page counts of the entry
    start_time = time.time() # start time
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(args, last_page, writer)) # run async fuction
    fp.close() # close file after finished scrape
    driver.close()
    driver.quit()
    now = datetime.now() # current time
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S") # date and time format
    print(f'[{dt_string}] '+ 'COMPLETED ' + f'Scrape took {time.time() - start_time} seconds.', f'Scraped {i} entries.') # print finish message
    