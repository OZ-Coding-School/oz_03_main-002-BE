import logging

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 로깅 설정 (파일과 콘솔에 모두 출력)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scraping.log"),  # 로그 파일 저장
        logging.StreamHandler(),  # 콘솔 출력
    ],
)

# 가상 디스플레이 설정
display = Display(visible=0, size=(1920, 1080))
display.start()

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


# 웹 드라이버 생성
driver = webdriver.Chrome(options=chrome_options)

# 원하는 웹 페이지 접속
url = "https://m.10000recipe.com/recipe/6855387"
logging.info(f"Accessing URL: {url}")
driver.get(url)

# 썸네일 이미지 불러오기
thumbnail_element = driver.find_element(By.CLASS_NAME, "view3_pic_img")
thumbnail_url = thumbnail_element.find_element(By.TAG_NAME, "img").get_attribute("src")
logging.info(f"Thumbnail URL: {thumbnail_url}")

# 재료 리스트 가져오기
ingre_dict = {}
ingre_elements = driver.find_elements(By.CSS_SELECTOR, ".ingre_list li")
for element in ingre_elements:
    ingre = element.find_element(By.TAG_NAME, "a").text
    ingre_ea = element.find_element(By.TAG_NAME, "span").text
    ingre_dict[ingre] = ingre_ea
logging.info(f"Ingredient List: {ingre_dict}")

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
    logging.info(f"Recipe Step {i+1}: {detail}")  # 각 단계별 정보 로깅

logging.info(f"Complete Recipe: {recipe}")  # 전체 레시피 로깅

# 웹 드라이버 종료
driver.quit()

# 가상 디스플레이 종료
display.stop()
