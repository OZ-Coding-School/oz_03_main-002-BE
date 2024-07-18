import json
from cryptography.fernet import Fernet

def load_config(config_file, key_file):
    with open(key_file, 'rb') as f:
        key = f.read()
    fernet = Fernet(key)

    with open(config_file, 'rb') as f:
        encrypted_config = f.read()
    decrypted_config = fernet.decrypt(encrypted_config)

    return json.loads(decrypted_config)

# 테스트를 위한 코드
config = load_config('config_test.json.enc', 'config.key')
# 본 코드
# config = load_config('config.json.enc', 'config.key')
endpoint = config['endpoint']
username = config['username']
password = config['password']

# RDS 연결 로직 (예시)
import psycopg2

conn = psycopg2.connect(
    host=endpoint,
    user=username,
    password=password,
)


# 대분류 코드 넣기
with open('../DataTools/Data/result/ingredients_major.json', 'r') as f :
    data = json.load(f)
cur = conn.cursor()
for item in data :
    code = data[item]['major_code']
    name = data[item]['major_name']
    cur.execute("INSERT INTO ingre_major (name, id) VALUES (%s, %s)", (name, code))
conn.commit()
print("데이터 삽입 완료")


# 중분류 코드 넣기
with open('../DataTools/Data/result/ingredients_middle.json', 'r') as f :
    data = json.load(f)
cur = conn.cursor()
temp = []
for item in data :
    code = data[item]['middle_code']
    name = data[item]['middle_name']
    major_code = data[item]['major_code']
    if code not in temp :
        cur.execute("INSERT INTO ingre_middle (name, id, major_id) VALUES (%s, %s, %s)", (name, code, major_code))
        print(name, code, major_code)
        temp.append(code)
        
conn.commit()
print("데이터 삽입 완료")


# 소분류 코드 넣기
with open('../DataTools/Data/result/ingredients_sub.json', 'r') as f :
    data = json.load(f)
cur = conn.cursor()
temp = []
for item in data :
    code = data[item]['sub_code']
    name = data[item]['sub_name']
    middle_code = data[item]['middle_code']
    if name == None :
        name = 'None'
    if code not in temp :
        cur.execute("INSERT INTO ingre_sub (name, id, middle_id) VALUES (%s, %s, %s)", (name, code, middle_code))
        print(name, code, middle_code)
        temp.append(code)
conn.commit()
print("데이터 삽입 완료")