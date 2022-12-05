from scraper_depth import *
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


f = open("seed_list.txt", "r")

title_path = '//*[@id="title"]/h1'
description_path = '//*[@id="description"]'

count = 38
for line in f:
    (tree, map, depth_dict) = create_tree(line[:-1], defaultdict(list))

    #url_list = defaultdict(tuple)
    #print(map)


    data = defaultdict(list)

    dive = 0
    dive_map = {0:[], 1:[], 2:[]}
    for pre, fill, node in RenderTree(tree):
        if node.name in map:
            dive_map[dive].append((map[node.name][0], map[node.name][2]))
        if not node.children:
            dive += 1
    
    json_object = json.dumps(dive_map, indent = 4) 
    file_name = "dfs_"+str(count)+".json"
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
    count+=1
    