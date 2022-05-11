import os
import time
from requests import auth
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver-manager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import authorization
import json

#Windows based settings
browser = webdriver.Chrome(ChromeDriverManager().install())


'''
##Unix based settings
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser= webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=options)
'''
login_info = authorization.user_info
chat = authorization.config['chat']
chat_token = authorization.config['chat_token']

try:
    for key,value in login_info.items():
        userID = key
        password = login_info[key]['password']
        pin = login_info[key]['otp']
        browser.get('https://kite.zerodha.com/')
        time.sleep(1)
        input = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@maxlength='6']")))
        input.clear()
        input.send_keys(userID)
        time.sleep(1)
        input = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@maxlength='260']")))
        input.clear()
        input.send_keys(password)
        time.sleep(1)
        sub_button = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='button-orange wide']")))
        sub_button.click()
        time.sleep(1)
        input = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@maxlength='6']")))
        input.clear()
        input.send_keys(pin)
        time.sleep(1)
        sub_button = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='button-orange wide']")))
        sub_button.click()
        time.sleep(1)
        curl=browser.current_url
        #print(browser.get_cookies())
        for item in range(len(browser.get_cookies())):
            if browser.get_cookies()[item]['name'] == 'enctoken':
                token = browser.get_cookies()[item]['value']
        if token:
            browser.close()
            authorization_token = "enctoken {0}"
            authorization_token = authorization_token.format(token)
            temp_dir = authorization.config['temp_path']
            for fname in os.listdir(temp_dir):
                if fname.startswith(userID):
                    os.remove(os.path.join(temp_dir, fname))
            with open(os.path.join(temp_dir, key + '.token'),'w') as token_file:
                token_file.write(authorization_token)
        else:
            chat_message = "empty token generated"
            chat_url = f'https://api.telegram.org/bot{chat_token}/sendMessage?chat_id={chat}&text={chat_message}'
except Exception as e:
    chat_message = "Exception Reason : "+ str(e)
    chat_url = f'https://api.telegram.org/bot{chat_token}/sendMessage?chat_id={chat}&text={chat_message}'


