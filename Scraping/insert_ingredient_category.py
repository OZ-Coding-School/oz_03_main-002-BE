import json
import os

import dotenv

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


# 대분류 코드 넣기
with open("../DataTools/Data/result/ingredients_major.json") as f:
    data = json.load(f)
cur = conn.cursor()
for item in data:
    code = data[item]["major_code"]
    name = data[item]["major_name"]
    cur.execute(
        "INSERT INTO ingredient_ingremajor (name, id) VALUES (%s, %s)", (name, code)
    )
conn.commit()
print("데이터 삽입 완료")


# 중분류 코드 넣기
with open("../DataTools/Data/result/ingredients_middle.json") as f:
    data = json.load(f)
cur = conn.cursor()
temp = []
for item in data:
    code = data[item]["middle_code"]
    name = data[item]["middle_name"]
    major_code = data[item]["major_code"]
    if code not in temp:
        cur.execute(
            "INSERT INTO ingredient_ingremiddle (name, id, major_id) VALUES (%s, %s, %s)",
            (name, code, major_code),
        )
        temp.append(code)

conn.commit()
print("데이터 삽입 완료")


# 소분류 코드 넣기
with open("../DataTools/Data/result/ingredients_sub.json") as f:
    data = json.load(f)
cur = conn.cursor()
temp = []
for item in data:
    code = data[item]["sub_code"]
    name = data[item]["sub_name"]
    middle_code = data[item]["middle_code"]
    if name == None:
        name = "None"
    if code not in temp:
        cur.execute(
            "INSERT INTO ingredient_ingresub (name, id, middle_id) VALUES (%s, %s, %s)",
            (name, code, middle_code),
        )
        temp.append(code)
conn.commit()
print("데이터 삽입 완료")
