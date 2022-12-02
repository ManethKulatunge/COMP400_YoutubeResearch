from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from anytree import Node, RenderTree, LevelOrderGroupIter
from collections import defaultdict
import time




def depth_first_search(driver, node, recommended_videos, depth):
    if depth == 5:
        return 
    current = node
    driver.implicitly_wait(5)
    time.sleep(1)
    driver.get(current.name)
    path = '//*[@id="related"]/ytd-watch-next-secondary-results-renderer//*[@id="thumbnail"]'
    time.sleep(1)
    driver.implicitly_wait(5)
    elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, path)))
    hrefs = [i.get_attribute('href') for i in elements]
    
    new_node_href = ''
    for href in hrefs:
        if not (href in recommended_videos) and not (href == None) and not ("googleadservices" in href) and not("show" in href):
            recommended_videos.append(href)
            new_node_href = href
            break
    
    depth_first_search(driver, Node(new_node_href, parent=current), recommended_videos, depth+1)
            



def create_tree(starter_video, tree_depth):
    driver = uc.Chrome()
    driver.implicitly_wait(30)

    first = Node(starter_video)
    node_list = [first]
    recommended_videos = [first.name]

    current = node_list.pop(0)
    driver.implicitly_wait(5)
    time.sleep(1)
    driver.get(current.name)
    path = '//*[@id="related"]/ytd-watch-next-secondary-results-renderer//*[@id="thumbnail"]'
    time.sleep(1)
    driver.implicitly_wait(5)
    elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, path))) #This is a dummy element)
    hrefs = [i.get_attribute('href') for i in elements]

    count = 0
    for href in hrefs:
        if count<3 and not (href in recommended_videos) and not (href == None) and not ("googleadservices" in href) and not("show" in href):
            node_list.append(Node(href, parent=current))
            recommended_videos.append(href)
            count+=1
        elif count == 3:
            break
    for video in node_list:
        depth_first_search(driver, video, [video.name, first.name], 1)
    
    for pre, fill, node in RenderTree(first):
        print("%s%s" % (pre, node.name))

    #tree_depth = [[node.name for node in children] for children in LevelOrderGroupIter(first)]
    
    #for i in range(len(tree_depth)):
    #    print('Level ' +str(i) + ':' + str(len(tree_depth[i])))

    driver.close()

    return node

create_tree("https://www.youtube.com/watch?v=t_CqAwkjiF4", defaultdict(list))