from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import psycopg2
import time
PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)
import json
url = 'https://psnprofiles.com/games'
driver.get(url)

# conn = psycopg2.connect("dbname=psnprofile user=postgres password=123456")
# cur = conn.cursor()

# create_table_query = '''CREATE TABLE Games
#             (ID INT PRIMARY KEY     NOT NULL,
#             NAME           TEXT    NOT NULL,
#             Bronze           INT     NOT NULL,
#             Silver           INT     NOT NULL,
#             Gold           INT     NOT NULL,
#             Platinum           INT     NOT NULL,
#             Total Trophies           INT     NOT NULL,'''

count = 0
games = []
current_page = 1
page = list(range(1, 362))
for pages in page:
    url = f"https://psnprofiles.com/games?page={pages}"
    driver.get(url)
    title = driver.find_elements(By.CLASS_NAME, "zebra")
    shown_titles = title
    for i, title in enumerate(title):
        table_header = driver.find_element(By.XPATH, "//html/body/div[4]/div[3]/div/div/div[1]/div[2]/div[1]/h3")
        if table_header is not None:
            driver.find_element(By.XPATH, "//table[@id='game_list']/tbody/tr[1]/td[2]/div/span")
            game = title.text
            games.append(game)
            if table_header != driver.find_element(By.CLASS_NAME, "grow"):
                break
            continue
    new_games = [games.split('\n') for games in games]
    list_games = [[item.replace(' • ', ' ') for item in game] for game in new_games]
    games_flat = [item for sublist in list_games for item in sublist]
    
    #print(games_flat)
    json_object = json.dumps(games_flat, indent = 2)
    
    with open("games.json", "a") as outfile:
        outfile.write(json_object) 
    while current_page != len(page):
        current_page +=1
        time.sleep(1)
        break
    if current_page == len(page):
        driver.quit()
        break
        





