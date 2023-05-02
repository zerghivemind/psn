from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/chromedriver.exe', options=chrome_options)
import json
import csv
import os
url = 'https://psnprofiles.com/games'
driver.get(url)
os.chdir('D:\\psntrophies')
class TrophyScraper:
    def __init__(self):
        self.clean_trophies = []
        self.trophy_tiers = []

    def scrape_trophies(self, driver):
        trophy_elements = driver.find_elements(By.CLASS_NAME, "zebra")

        for trophy in trophy_elements:
            td_elements = trophy.find_elements(By.TAG_NAME, 'td')
            span_elements = trophy.find_elements(By.CSS_SELECTOR, 'td:nth-child(6) > span')
            trophy_text = []
            for td in td_elements:
                trophy_text.append(td.text.strip())
            
            self.clean_trophies.append(trophy_text)
                                
            for span in span_elements:
                trophy_rarity = span.find_element(By.TAG_NAME , 'img').get_attribute('title')
                self.trophy_tiers.append(trophy_rarity)
                
        return self.clean_trophies, self.trophy_tiers 
    
scraper = TrophyScraper()

def get_links(driver):
    link_titles = []
    title_elements = driver.find_elements(By.CLASS_NAME, "zebra")
    for i, title_element in enumerate(title_elements):
        link_elements = title_element.find_elements(By.CSS_SELECTOR, "span a")
        for link in link_elements:
            link_title = link.get_attribute("href")
            if link_title not in link_titles:
                link_titles.append(link_title)
    return link_titles

count = 0
games = []
trophy_tier_list = []
cleaned_trophies_list = []
game_ids = []
gametitle = []

link_count = 0
link_titles = []
all_game_data = []

url = f"https://psnprofiles.com/games?page={1}"
driver.get(url)
link_titles = get_links(driver)
time.sleep(2)

for link in link_titles:
    driver.get(link)
    time.sleep(2)
                        
    data = {
        "gameids": [],
        "gametitle": [],
        "cleaned_trophies": [],
        "trophy_tier": []
    }

    get_url = driver.current_url
    game_id_title = get_url.split("/")[-1]
    game_id = game_id_title.split("-")[0]
    game_ids.append(game_id)
    title_elements = driver.find_elements(By.CSS_SELECTOR, ".title.flex.v-align.center")
    for title_element in title_elements:
        h3_element = title_element.find_element(By.TAG_NAME, "h3")
        title = h3_element.text
        titles = title.split()
        gametitle.append(titles)
    #DLC check
    dlc_elements = driver.find_elements(By.CSS_SELECTOR, "[id^='DLC-']")
    for element in dlc_elements:
        dlc_title_element = element.find_element(By.TAG_NAME, "h3")
        dlc_title = dlc_title_element.text
        gametitle.append(dlc_title)
        
    trophy_data = scraper.scrape_trophies(driver)
    cleaned_trophies_list.append(trophy_data[0])
    trophy_tier_list.append(trophy_data[1])
    data["cleaned_trophies"] = [cleaned_trophies_list]
    data["trophy_tier"] = [trophy_tier_list]
    data["gameids"] = [game_ids]
    data["gametitle"] = [gametitle]
    
    # append the data for the current game to the overall lists
    games.append(data)



with open("psngametrophies.json", "w") as f:
    json.dump(games, f)


        
            
        
        
    
        
        

