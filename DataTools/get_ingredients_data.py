import json
import os

import pandas as pd

# 결과 생성 폴더
os.makedirs("Data/result", exist_ok=True)

# 식재료
df = pd.read_csv("Data/ingredients.csv", encoding="cp949")
df_deduplicated = df.drop_duplicates(subset=["대표식품명"], keep="first")
df_deduplicated = df_deduplicated[
    [
        "식품명",
        "식품대분류코드",
        "식품대분류명",
        "식품중분류코드",
        "식품중분류명",
        "식품소분류코드",
        "식품소분류명",
    ]
].reset_index(drop=True)
df_deduplicated = df_deduplicated.replace("해당없음", None)

# 대분류 코드
major_code = (
    df_deduplicated[["식품대분류코드", "식품대분류명"]]
    .drop_duplicates(subset="식품대분류명", keep="first")
    .reset_index(drop=True)
)
major_code = major_code.rename(
    columns={"식품대분류코드": " major_code", "식품대분류명": "major_name"}
)
result_dict = major_code.to_dict(orient="index")
result_json = json.dumps(result_dict, ensure_ascii=False)
with open("Data/result/ingredients_major.json", "w", encoding="utf-8") as f:
    f.write(result_json)

# 중분류 코드
middle_code = (
    df_deduplicated[["식품중분류코드", "식품중분류명"]]
    .drop_duplicates(subset="식품중분류명", keep="first")
    .reset_index(drop=True)
)
middle_code = middle_code.rename(
    columns={"식품중분류코드": " middle_code", "식품중분류명": "middle_name"}
)
result_dict = middle_code.to_dict(orient="index")
result_json = json.dumps(result_dict, ensure_ascii=False)
with open("Data/result/ingredients_middle.json", "w", encoding="utf-8") as f:
    f.write(result_json)

# 소분류 코드
sub_code = (
    df_deduplicated[["식품소분류코드", "식품소분류명"]]
    .drop_duplicates(subset="식품소분류명", keep="first")
    .reset_index(drop=True)
)
sub_code = sub_code.rename(
    columns={"식품소분류코드": " sub_code", "식품소분류명": "sub_name"}
)
result_dict = sub_code.to_dict(orient="index")
result_json = json.dumps(result_dict, ensure_ascii=False)
with open("Data/result/ingredients_sub.json", "w", encoding="utf-8") as f:
    f.write(result_json)

# 식재료 명 추출을 위한 전처리
df_deduplicated["식품명"] = df_deduplicated["식품명"].astype(str).str.split("것").str[0]
df_deduplicated["식품명"] = (
    df_deduplicated["식품명"].astype(str).str.split("전체").str[0]
)
df_deduplicated["식품명"] = df_deduplicated["식품명"].astype(str).str.split("_").str[0]
sub_code = df_deduplicated.rename(
    columns={
        "식품명": "ingredients_name",
        "식품대분류코드": "major_code",
        "식품대분류명": " major_name",
        "식품중분류코드": "middle_code",
        "식품중분류명": "middle_name",
        "식품소분류코드": "sub_code",
        "식품소분류명": "sub_name",
    }
)
result_dict = sub_code.to_dict(orient="index")
result_json = json.dumps(result_dict, ensure_ascii=False)
with open("Data/result/ingredients_list.json", "w", encoding="utf-8") as f:
    f.write(result_json)
