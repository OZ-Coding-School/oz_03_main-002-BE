import json


import dotenv
import os

dotenv.load_dotenv("../Django/.env")


# 본 코드
# config = load_config('config.json.enc', 'config.key')
endpoint = os.getenv("RDS_HOSTNAME")
username = os.getenv("RDS_USERNAME")
password = os.getenv("RDS_PASSWORD")

# RDS 연결 로직 (예시)
import psycopg2

conn = psycopg2.connect(
    host=endpoint,
    user=username,
    password=password,
)

# 요리 종류 리스트
with open("../DataTools/Data/result/cooking_type_list.json", "r") as f:
    data = json.load(f)
cur = conn.cursor()
for item in data:
    cur.execute(f"INSERT INTO recipe_cookingtype (name) VALUES ('{data[item]}')")
conn.commit()
print("데이터 삽입 완료")

# 요리 상황 리스트
with open("../DataTools/Data/result/cooking_situation_list.json", "r") as f:
    data = json.load(f)
cur = conn.cursor()
for item in data:
    cur.execute(f"INSERT INTO recipe_cookingsituation (name) VALUES ('{data[item]}')")
conn.commit()
print("데이터 삽입 완료")

# 요리 방법 리스트
with open("../DataTools/Data/result/cooking_methods_list.json", "r") as f:
    data = json.load(f)
cur = conn.cursor()
for item in data:
    cur.execute(f"INSERT INTO recipe_cookingmethod (name) VALUES ('{data[item]}')")
conn.commit()
print("데이터 삽입 완료")


# 요리 주재료 리스트
with open("../DataTools/Data/result/cooking_main_ingredients_list.json", "r") as f:
    data = json.load(f)
cur = conn.cursor()
for item in data:
    cur.execute(f"INSERT INTO recipe_cookingmainingre (name) VALUES ('{data[item]}')")
conn.commit()
print("데이터 삽입 완료")
