import json

from cryptography.fernet import Fernet


def load_config(config_file, key_file):
    with open(key_file, "rb") as f:
        key = f.read()
    fernet = Fernet(key)

    with open(config_file, "rb") as f:
        encrypted_config = f.read()
    decrypted_config = fernet.decrypt(encrypted_config)

    return json.loads(decrypted_config)


# 테스트를 위한 코드
config = load_config("config_test.json.enc", "config.key")
# 본 코드
# config = load_config('config.json.enc', 'config.key')
endpoint = config["endpoint"]
username = config["username"]
password = config["password"]

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
    cur.execute(f"INSERT INTO cooking_type (name) VALUES ('{data[item]}')")
conn.commit()
print("데이터 삽입 완료")

# 요리 상황 리스트
with open("../DataTools/Data/result/cooking_situation_list.json", "r") as f:
    data = json.load(f)
cur = conn.cursor()
for item in data:
    cur.execute(f"INSERT INTO cooking_type (name) VALUES ('{data[item]}')")
conn.commit()
print("데이터 삽입 완료")

# 요리 방법 리스트
with open("../DataTools/Data/result/cooking_methods_list.json", "r") as f:
    data = json.load(f)
cur = conn.cursor()
for item in data:
    cur.execute(f"INSERT INTO cooking_type (name) VALUES ('{data[item]}')")
conn.commit()
print("데이터 삽입 완료")


# 요리 주재료 리스트
with open("../DataTools/Data/result/cooking_main_ingredients_list.json", "r") as f:
    data = json.load(f)
cur = conn.cursor()
for item in data:
    cur.execute(f"INSERT INTO cooking_type (name) VALUES ('{data[item]}')")
conn.commit()
print("데이터 삽입 완료")
