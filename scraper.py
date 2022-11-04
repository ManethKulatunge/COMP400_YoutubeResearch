from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install()) 
driver.implicitly_wait(60)
driver.get("https://www.youtube.com/watch?v=bldBqtgAX2o")

user_data = driver.find_elements(By.ID, 'video-title')
print(user_data)
links = []
for i in user_data:
            links.append(i.get_attribute('href'))

print(len(links))