from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ChromedriverDownloader import * # type: ignore
download_chromedriver("", "", latest_chromedriver(), False) # type: ignore

account = str(input("Please Provide Username Of Account You Wanna Archive Messages Of: "))

print("\nRunning posts-archiver.py...\n")

import time
from colorama import *
from datetime import datetime

init()

driver = webdriver.Chrome()

delay = 60
wait = WebDriverWait(driver, delay)

driver.get(f"https://krunker.io/social.html?p=profile&q={account}")

current_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")

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

def archive_messages():
    feed_tab = wait.until(EC.visibility_of_element_located((By.ID, "pTab_activity")))
    feed_tab.click()

    posts = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "socPost")))
    
    for post in posts:
        try:
            with open(f"Archiver Messages/{current_time}/{account}.txt", "a", encoding="utf-8") as archive:
                driver.execute_script("arguments[0].scrollIntoView();", post)
                post_info = post.find_element(By.CLASS_NAME, "postInfo")
                post_content = post.find_element(By.CLASS_NAME, "postContent")

                info = post_info.text.split("\n")
                user, time, followers = info[0], info[1], info[2]
                content = post_content.text

                if not "Rank Name Score Kills Deaths Reward" in content:
                    user_content_info = f"{user} | {time} | {followers} | Content: {content}"
                    archive.write(f"\n{user_content_info}\n")
                else:
                    content = content.replace("Rank Name Score Kills Deaths Reward", "")

                    rank_info = f"{user} | {time} | {followers}\n\nRank | Name | Score | Kills | Deaths | Reward {content}"

                    archive.write(f"\n{rank_info}\n")

        except Exception as e:
            print("Couldn't retrieve post info:", e)

    
    
def main():
        try:
            time.sleep(5)
            archive_messages()
        except Exception as e:
                print(e)
                driver.quit()

if __name__ == "__main__":
    accept_button = wait.until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
    accept_button.click()

    try:
        account_information = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@style="font-size:20px;color:rgba(255,255,255,0.5)"]')))
        
        if "Profile doesn't exist" in account_information.text:
            input("Please provide correct username. Press ENTER to leave.")
            exit()

    except Exception as e:
        pass

    os.makedirs(f"Archiver Messages/{current_time}" ,exist_ok=True)
    if not os.path.exists(f"Archiver Messages/{current_time}/{account}.txt"):
        open(f"Archiver Messages/{current_time}/{account}.txt", "w", encoding="utf-8").close()

    main()

driver.close()