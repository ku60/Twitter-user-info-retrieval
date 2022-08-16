import gspread
from gspread.exceptions import *
from oauth2client.service_account import ServiceAccountCredentials
import sys
from selenium import webdriver
import time

"""
sleep time depends on your network
if you have a bad connection, plese increase the parameter of time.sleep()

"""

def ChromeDriver_setup(user_agent):
    options = webdriver.ChromeOptions()
    options.add_argument("--user-agent :" + user_agent)
    return options


def login(user_name, password):
    login_button = driver.find_element("xpath", '/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div')
    login_button.click()
    time.sleep(1)
    user_name_form = driver.find_element("xpath", '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    user_name_form.send_keys(user_name)
    next_button = driver.find_element("xpath", '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    next_button.click()
    time.sleep(1)
    password_form = driver.find_element("xpath", '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
    password_form.send_keys(password)
    time.sleep(1)
    login_conf = driver.find_element("xpath", '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
    login_conf.click()


def ret_account_info(account_name):
    ac_url = url + account_name
    driver.get(ac_url)
    time.sleep(4)
    
    #when the NFT profile pop up shown
    try:
        OK_button = driver.find_element("xpath", "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div")
        OK_button.click()
        time.sleep(2)
    except:
        pass
    
    #when sensitive content caution shown
    try:
        view_prof_button = driver.find_element("xpath", "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/div/div[3]")
        view_prof_button.click()
        time.sleep(2)
    except:
        pass
    
    following = driver.find_element("xpath", '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[1]/a/span[1]/span')
    following_num = following.text
    follower = driver.find_element("xpath", '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span')
    follower_num = follower.text
    res_list = []
    for f in [following_num, follower_num]:
        if "K" in f:
            f = float(f.replace("K", ""))
            f = int(f*1000)
        elif "M" in f:
            f = float(f.replace("M", ""))
            f = int(f*1000000)
        elif "," in f:
            f = float(f.replace(",",""))
            f = int(f)
        else:
            f = int(f)
        res_list.append(f)
    ff_ratio = res_list[0]/res_list[1]
    likes = driver.find_element("xpath", "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/nav/div/div[2]/div/div[4]/a")
    likes.click()
    time.sleep(2)
    
    #when sensitive content caution shown
    try:
        view_prof_button = driver.find_element("xpath", "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/div/div[3]")
        view_prof_button.click()
        time.sleep(2)
    except:
        pass
    
    activity = driver.find_element("xpath", "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div[3]/a/time")
    date = activity.get_attribute("datetime")
    return(account_name, ac_url, following_num, follower_num, ff_ratio, date)


def next_available_row(worksheet, col_num):
    str_list = list(filter(None, worksheet.col_values(col_num))) 
    return str(len(str_list) + 1)


def get_gspread_book(secret_key, book_name):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(secret_key, scope)
    gc = gspread.authorize(credentials)
    book = gc.open(book_name)
    return book

def write_data(account_name, sheet, col_num, row):
    """
    pass the int correspond to column you want to start writing data
    column "A" corresponds to 0, "B":1, ...
    ex) if you want to start with column "C", pass 2 as start_chr
    
    ASCII code point "a" corresponds to 97 and "z" to 122
    you need to make sure 0 <= col_num <= 20
    """ 
    name, ac_url, fing, fer, ff, date = ret_account_info(account_name)
    sheet.update_acell(chr(col_num+96)+str(row), name)
    sheet.update_acell(chr(col_num+97)+str(row), ac_url)
    sheet.update_acell(chr(col_num+98)+str(row), fing)
    sheet.update_acell(chr(col_num+99)+str(row), fer)
    sheet.update_acell(chr(col_num+100)+str(row), ff)
    sheet.update_acell(chr(col_num+101)+str(row), date)



if __name__ = "__main__" :
    user_agent = "write your own user agent"
    driver_path = "write your own driver path"
    url = "https://twitter.com/"
    user_name = "write your own test account name"
    password = "the accouts' password"

    secret_key = "write your own secret key pass"
    book_name = 'ex) Twitter_user_info_list'
    sheet_name = "ex) sheet1"
    
    accoount_name = "write account name you want to know"
    col_num = "write column number (start with one, A:1, B:2, ...) you want to start writing the data as int type"
    row = "write row number you want to start writing the data as int type"
    
    options = ChromeDriver_setup(user_agent)
    driver = webdriver.Chrome(driver_path, chrome_options=options)
    driver.get(url)
    time.sleep(2)
    start_ChromeDriver(user_agent, driver_path, url)
    
    try:
        sheet = get_gspread_book(secret_key, book_name).worksheet(sheet_name)
    except SpreadsheetNotFound:
        print('Spreadsheet: ' + book_name + 'NotFound')
        sys.exit()
    except WorksheetNotFound:
        print('Worksheet: ' + sheet_name + 'NotFound')
        sys.exit()
    
    write_data(account_name, sheet, col_num, row)