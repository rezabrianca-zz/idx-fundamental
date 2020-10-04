#!/usr/bin/python3
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd
import time
import os

os.getcwd()
today = pd.to_datetime('today').strftime('%Y-%m-%d')
print('Begin job at {0}'.format(today))

# setup
opts = Options()
opts.add_argument('log-level=3') # suppress warning
opts.add_argument('--no-sandbox')

# remove comment and change the path to your chromedriver directory
# browser = Chrome('/Users/username/Downloads/chromedriver', options=opts)

browser.implicitly_wait(1)

try:
    # open web page
    browser.get('https://www.idx.co.id/perusahaan-tercatat/profil-perusahaan-tercatat/')

    # select page to display 100 company in a page
    select = Select(browser.find_element_by_name('companyTable_length'))
    number_per_page = int(select.options[3].text)
    select.select_by_value('100')
    time.sleep(0.5)

    company_df = pd.DataFrame()

    # get page number to fetch
    page_element = browser.find_elements_by_class_name('paginate_button ')
    page_element_length = len(page_element) + 1 # to capture last page
    time.sleep(0.5)

    # retrieve data in the each page
    for i in range(1, page_element_length):
        try:
            print('Retrieve data in page {0} ...'.format(i))
            next = browser.find_elements_by_xpath('/html/body/main/div[2]/div/div[2]/div/div[4]/a[2]')[0].click()
            company_table = browser.find_element_by_id('companyTable').text.split('\n')
            company_raw = [company_table[i].split() for i in range(1, len(company_table))]
            company_code = [company_raw[i][1] for i in range(len(company_raw))]
            company_name = [' '.join(company_raw[i][2:-3]) for i in range(len(company_raw))]
            date_public = [' '.join(company_raw[i][-3:]) for i in range(len(company_raw))]
            company_df_add = pd.DataFrame({'Kode':company_code, 'Nama':company_name, 'Tanggal Pencatatan':date_public})

            # append company information
            company_df = company_df.append(company_df_add, ignore_index=True)
            time.sleep(1)

        except ElementClickInterceptedException:
            element = browser.find_element_by_class_name("paginate_button next")
            browser.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)
            print(element)

    # store in csv
    company_df.to_csv('./data/company_code_{0}.csv'.format(today), index=False)
    print('There are {0} public companies at {1}'.format(company_df.shape[0], today))

finally:
    # close the browser
    browser.close()
    quit()
