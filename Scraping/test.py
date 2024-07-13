import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from pyvirtualdisplay import Display #For Linux Server

import json


# 로깅 설정 (파일과 콘솔에 모두 출력)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scraping.log"),  # 로그 파일 저장
        logging.StreamHandler()  # 콘솔 출력
    ],
)

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--incognito")


# 웹 드라이버 생성
driver = webdriver.Chrome(options=chrome_options)


with open('Data/preprocessed_data.json', 'r') as f :
    data = json.load(f)
    
    
for num in data :
    logging.info(f"Scaping : {num} recipe")
    if data[num]['thumbnail_url'] == None or data[num]['ingre_list'] == None or data[num]['detail_recipes'] == None :
        try :
            url = data[num]['URL']
            logging.info(f"Accessing URL: {url}")
            driver.get(url)
                
            # 썸네일 이미지 불러오기
            thumbnail_element = driver.find_element(By.CLASS_NAME, "view3_pic_img")
            thumbnail_url = thumbnail_element.find_element(By.TAG_NAME, "img").get_attribute("src")
            data[num]['thumbnail_url'] = thumbnail_url
            logging.info("Thumbnail URL Done")

            # 재료 리스트 가져오기
            ingre_dict = {}
            ingre_elements = driver.find_elements(By.CSS_SELECTOR, ".ingre_list li")
            for element in ingre_elements:
                ingre = element.find_element(By.TAG_NAME, "a").text
                ingre_ea = element.find_element(By.TAG_NAME, "span").text
                ingre_dict[ingre] = ingre_ea
            data[num]['ingre_list'] = ingre_dict
            logging.info("Ingredient List Done")

            # 레시피 가져오기
            recipe = {}
            recipe_elements = driver.find_elements(By.CSS_SELECTOR, ".step_list.st_thumb li")
            for i, element in enumerate(recipe_elements):
                detail = {}
                detail_recipe = element.find_element(By.CSS_SELECTOR, ".step_list_txt_cont")
                detail["recipe"] = detail_recipe.text

                try:
                    detail_tip = element.find_element(By.CSS_SELECTOR, ".step_list_txt_tip")
                    detail["tip"] = detail_tip.text
                except:
                    detail["tip"] = ""

                try:
                    detail_img = element.find_element(By.CSS_SELECTOR, ".step_list_txt_pic img")
                    detail["img_url"] = detail_img.get_attribute("src")
                except:
                    detail["img_url"] = ""

                recipe[str(i + 1)] = detail

            logging.info("Complete Recipe")  # 전체 레시피 로깅
            data[num]['detail_recipes'] = recipe
        except :
            with open('Data/preprocessed_data.json', 'w') as f :
                json.dump(data, f, indent=4)
            with open('Data/Fail.json', 'a') as f :
                json.dump(num, f, indent=4)    
            continue
        if int(num)%1000 == 0 :
            with open('Data/preprocessed_data.json', 'w') as f :
                json.dump(data, f, indent=4)
    else :
        logging.info('Completed Recipe')