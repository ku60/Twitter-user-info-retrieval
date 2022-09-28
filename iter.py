"""
please use the same layout with my sample Spread Sheet
"""

import gspread
from gspread.exceptions import *
from oauth2client.service_account import ServiceAccountCredentials
import sys
from selenium import webdriver
import time

import utils

if __name__ = "__main__" :
    user_agent = "write your own user agent"
    driver_path = "write your own driver path"
    url = "https://twitter.com/"
    user_name = "write your own test account name"
    password = "the accouts' password"

    secret_key = "write your own secret key pass"
    book_name = 'ex) Twitter_account_info_list'
    sheet_name = "ex) sheet1"
    
    accoount_name = "write account name you want to know"
    accout_name_col = "write column number (start with one, A:1, B:2, ...) account data are written as int type (in the sample sheet, 3)"
    
    
    
    options = utils.ChromeDriver_setup(user_agent)
    driver = webdriver.Chrome(driver_path, chrome_options=options)
    driver.get(url)
    time.sleep(2)
    utils.login(user_name, password)
    
    
    try:
        sheet = utils.get_gspread_book(secret_key, book_name).worksheet(sheet_name)
    except SpreadsheetNotFound:
        print('Spreadsheet: ' + book_name + 'NotFound')
        sys.exit()
    except WorksheetNotFound:
        print('Worksheet: ' + sheet_name + 'NotFound')
        sys.exit()
    
    for i in range(int(utils.next_available_row(sheet, account_name_col+1)), int(utils.next_available_row(sheet, account_name_col))):
        account_name = sheet.cell(i, account_name_col).value
        row = utils.next_available_row(sheet, account_name_col+1)
        utils.write_data(account_name, sheet, account_name_col, row)
