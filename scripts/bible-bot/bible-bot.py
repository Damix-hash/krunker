from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ChromedriverDownloader import * # type: ignore
download_chromedriver("", "", latest_chromedriver(), False) # type: ignore

print("\nRunning bible-bot.py...\n")

import time
import json
import random
import requests

quotes = []

response = requests.get("https://raw.githubusercontent.com/Damix-hash/bible-quotes/main/1126-Bible-Quotes.txt")

if response.ok:
    for line in response.text.split("\n"):
        if not '"' in line and not "'" in line:
            quotes.append(line)

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

def send(message):
    input_message = wait.until(EC.visibility_of_element_located((By.ID, "postInput")))
    send_message = wait.until(EC.visibility_of_element_located((By.ID, "postButton")))

    cprint("green", ">", f"Sending: {message}")

    input_message.send_keys(str(message))

    send_message.click()
    
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".lds-rings")))
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".lds-rings")))
    except TimeoutException:
        input_message.clear()
        pass

    try:
        message_popup = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, "genericPop")))
        if message_popup.is_displayed():
            message_response = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//div[@style="font-size:20px;color:rgba(255,255,255,0.5)"]')))
            cprint("red", "!", message_response.text)
            hide_popup = driver.find_element(By.ID, "popupBack")
            time.sleep(2)
            hide_popup.click

    except TimeoutException:
        pass
    
    input_message.clear()

def main():
        try:
            time.sleep(5)

            while True:
                msg = random.choice(quotes)
                send(msg.replace("god", "G0d"))

        except Exception as e:
                print(e)
                driver.quit()

if __name__ == "__main__":
    login_to_krunker(user, passw)
    main()
