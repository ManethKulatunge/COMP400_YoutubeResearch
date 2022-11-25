from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from anytree import Node, RenderTree
import time

driver = uc.Chrome()
driver.implicitly_wait(30)

first = Node("https://www.youtube.com/watch?v=t_CqAwkjiF4")
node_list = [first]
recommended_videos = [first.name]

#elements = driver.find_elements(By.XPATH, '//*[@id="dismissible"]/div/div[1]/a')
iterations = 0
while(node_list and iterations<20):
    current = node_list.pop(0)
    driver.implicitly_wait(5)
    time.sleep(1)
    driver.get(current.name)
    path = '//*[@id="related"]/ytd-watch-next-secondary-results-renderer//*[@id="thumbnail"]'
    #elements = driver.find_elements(by= By.XPATH, value= path)
    time.sleep(1)
    driver.implicitly_wait(5)
    elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, path))) #This is a dummy element)
    hrefs = [i.get_attribute('href') for i in elements]

    #hrefs = [video.get_attribute('href') for video in elements]
    count = 0
    for href in hrefs:
        if count<3 and not (href in recommended_videos) and not (href == None) and not ("googleadservices" in href) and not("show" in href):
            node_list.append(Node(href, parent=current))
            recommended_videos.append(href)
            count+=1
    for pre, fill, node in RenderTree(first):
        print("%s%s" % (pre, node.name))
    iterations += 1

for pre, fill, node in RenderTree(first):
    print("%s%s" % (pre, node.name))

driver.close()
    
