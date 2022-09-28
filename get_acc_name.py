import gspread
from gspread.exceptions import *
from oauth2client.service_account import ServiceAccountCredentials
import sys
from selenium import webdriver
import time

import utils


if __name__ == "__main__":
    account_name_col = "write column number (start with one, A:1, B:2, ...) account name are written as int type (in the sample sheet, 3)"
    target_acc_col = "write column number of account you want check following as int type *avoid private account"

    following_num = int(sheet.cell(target_acc_col,5).value)
    ret_account = sheet.cell(target_acc_col,4).value


    driver.get(ret_account)

    driver.get(ret_account + "/following")
    time.sleep(4)
    count = 0

    try:
        sheet = utils.get_gspread_book(secret_key, book_name).worksheet(sheet_name)
    except SpreadsheetNotFound:
        print('Spreadsheet: ' + book_name + 'NotFound')
        sys.exit()
    except WorksheetNotFound:
        print('Worksheet: ' + sheet_name + 'NotFound')
        sys.exit()


    for i in range(1,following_num+1):
        try:
            account = driver.find_element("xpath", f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[{i}]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span")
            account_name = account.text.replace("@","")
            row = utils.next_available_row(sheet, account_name_col)
            cell = chr(col_num+96) + row
            sheet.update_acell(cell, account_name)
            if int(sheet.cell(int(row), 2).value)>=2 :
                sheet.delete_row(int(row)) 

        except:
            pass
        count += 1
        #scroll to load
        if count == 7:
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(6)
            count = 0
