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
config = load_config("../crypto_files/config_test.json.enc", "config.key")
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


# 재료 목록 넣기
with open("../DataTools/Data/result/ingredients_list.json") as f:
    data = json.load(f)
cur = conn.cursor()
for item in data:
    major_id = data[item]["major_code"]
    middle_id = data[item]["middle_code"]
    sub_id = data[item]["sub_code"]
    name = data[item]["ingredients_name"]
    cur.execute(
        "INSERT INTO ingredient (name, major_id, middle_id, sub_id) VALUES (%s, %s, %s, %s)",
        (name, major_id, middle_id, sub_id),
    )
conn.commit()
print("데이터 삽입 완료")
