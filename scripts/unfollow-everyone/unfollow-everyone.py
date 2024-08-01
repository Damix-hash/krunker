'''
Unfollow-everyone.py.py Made By Damix
https://github.com/Damix-hash

TODO:
- Nothing

'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ChromedriverDownloader import * # type: ignore
download_chromedriver("", "", latest_chromedriver(), False) # type: ignore

print("\nRunning unfollow-everyone.py...\n")

import time
import json
from colorama import *

init()

with open("login.json", "r") as login:
    data = json.load(login)

user = data["username"]
passw = data["password"]

driver = webdriver.Chrome()

delay = 60
wait = WebDriverWait(driver, delay)

driver.get("https://krunker.io/social.html") 

def cprint(color=None, sign=None, msg=None, width=None):
    if msg is not None:
        if color is not None:
            color = color.lower()
            if color == "red":
                print("["+ Fore.RED + sign + Fore.RESET + "]", msg)
            elif color == "yellow":
                print("["+ Fore.YELLOW + sign + Fore.RESET + "]", msg)
            elif color == "green":
                print("["+ Fore.GREEN + sign + Fore.RESET + "]", msg)
        else:
            if width is not None:
                print(msg.center(int(width)))
            else:
                print(msg)
    else:
        print()

def login_to_krunker(user, passw):
    cprint("green", ">", "Logging into your krunker account!")

    accept_button = wait.until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
    accept_button.click()

    profileLogin = driver.find_element(By.ID, "profileLogin")
    profileLogin.click()

    login = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".accBtn.button.buttonG")))
    username = driver.find_element(By.ID, 'accName')
    password = driver.find_element(By.ID, 'accPass')

    username.send_keys(user)
    password.send_keys(passw)

    login.click()

    popup = driver.find_element(By.ID, "popupBack")
    popup.click()

def enter_following():
    profile = driver.find_element(By.ID, "profileImg")
    profile.click()

    time.sleep(10)

    check_following =  wait.until(EC.visibility_of_element_located((By.ID, "followC")))
    check_following.click()

def unfollow():
    unfollow_button = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "reqFollB.buttonR")))

    for button in unfollow_button:
        try:
            time.sleep(2)
            driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
        except Exception as e:
            print(e)
def main():
        try:
            time.sleep(10)
            enter_following()
            unfollow()
        except Exception as e:
                print(e)
                driver.quit()

if __name__ == "__main__":
    login_to_krunker(user, passw)
    main()
