from scraper_breadth import *
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from anytree import Node, RenderTree, LevelOrderGroupIter
from collections import defaultdict
import time
import json

f = open("seed_list_2.txt", "r")

title_path = '//*[@id="title"]/h1'
description_path = '//*[@id="description"]'

count = 42
for line in f:
    (tree, map) = create_tree(line[:-1], defaultdict(list))

    driver = uc.Chrome()
    driver.implicitly_wait(30)

    url_list = defaultdict(tuple)

    for level in map:
        for video in level:
            driver.implicitly_wait(5)
            time.sleep(1)
            driver.get(video)
            title_list = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, title_path)))
            title = title_list[0].text

            description_list = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, description_path)))
            description_temp = description_list[1].text
            description_arr = description_temp.split("\n")
            if (description_arr):
                description_arr.pop(0)
            if (description_arr):
                description_arr.pop(-1)
            description = "".join(description_arr)

            url_list[video] = (title,description)
    driver.close()


    data = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: []
    }

    for level in range(len(map)):
        for video in map[level]:
            if level in data:
                data[level].append({
                    'url': video,
                    'title': url_list[video][0],
                    'description': url_list[video][1]
                })
    
    json_object = json.dumps(data, indent = 4) 
    file_name = "bfs_"+str(count)+".json"
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
    
    count+=1
    