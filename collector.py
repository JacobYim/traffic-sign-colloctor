from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import chromedriver_autoinstaller
import requests
import os


if not "img" in os.listdir() :
    os.mkdir('img')
    
chromedriver_autoinstaller.install()
webpage_list = [
    # "https://www.trafficsigns.com/parking-signs",
    "http://www.hallsigns.com/signs/traffic-signs"
]

if __name__ == "__main__" :
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    driver = webdriver.Chrome(chrome_options=chrome_options)
    for webpage_url in webpage_list :
        driver.get(webpage_url)
        categories_url_list = list(map(lambda x : x.get_attribute('href'), driver.find_elements_by_class_name("item-inner")))
        for categories_url in categories_url_list :
            driver.get(categories_url)
            
            pages = list(set(map(lambda x : x.get_attribute('href'), driver.find_elements_by_class_name("pagination-link"))))
            pages.sort()
            for page in pages :
                driver.get(page)
                current_image_object_list = list(map(lambda x : x.find_element_by_tag_name('img'),driver.find_elements_by_class_name("card-img-container")))
                for current_image_object in current_image_object_list :
                    url = current_image_object.get_attribute('src')
                    data = requests.get(url).content
                    local_filename = 'img/'+current_image_object.get_attribute('title').replace("/", "_")
                    with open (local_filename, 'wb') as f:
                        f.write(data)

    driver.quit()
    