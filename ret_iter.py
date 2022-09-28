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

if __name__ == "__main__" :
    user_agent = input("write your own user agent >> ")
    driver_path = input("write your own driver path >> ")
    url = "https://twitter.com/"
    user_name = input("write your own test account name >> ")
    password = input("the accouts' password >> ")

    secret_key = input("write your own secret key path >> ")
    book_name = input("write book name ex) Twitter_account_info_list >> ")
    sheet_name = input("write sheeet name ex) sheet1 >> ")
    
    account_name_col = input("write column number (start with one, A:1, B:2, ...) account name is written as int type (in the sample sheet: 3) >> ")
    
    target_row = input("write row number written account you want to check following is written >> ")
    
    options = utils.ChromeDriver_setup(user_agent)
    driver = webdriver.Chrome(driver_path, chrome_options=options)
    driver.get(url)
    time.sleep(2)
    utils.login(user_name, password, driver)
    
    
    try:
        sheet = utils.get_gspread_book(secret_key, book_name).worksheet(sheet_name)
    except SpreadsheetNotFound:
        print('Spreadsheet: ' + book_name + 'NotFound')
        sys.exit()
    except WorksheetNotFound:
        print('Worksheet: ' + sheet_name + 'NotFound')
        sys.exit()
        
    #list account names up
    get_account_name(target_row, account_name_col, sheet, driver)
    
    
    #retrive account info
    for i in range(int(utils.next_available_row(sheet, account_name_col+1)), int(utils.next_available_row(sheet, account_name_col))):
        account_name = sheet.cell(i, account_name_col).value
        row = utils.next_available_row(sheet, account_name_col+1)
        utils.write_data(account_name, sheet, account_name_col, row, driver)
