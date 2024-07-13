import json
import os

import pandas as pd

# 결과 생성 폴더
os.makedirs("Data/result", exist_ok=True)
df = pd.read_csv("Data/recipe.csv", encoding="cp949", encoding_errors="ignore")
recipe_df = df[
    [
        "RCP_SNO",
        "RCP_TTL",
        "CKG_NM",
        "RGTR_NM",
        "INQ_CNT",
        "CKG_MTH_ACTO_NM",
        "CKG_STA_ACTO_NM",
        "CKG_MTRL_ACTO_NM",
        "CKG_KND_ACTO_NM",
        "CKG_IPDC",
        "CKG_INBUN_NM",
        "CKG_DODF_NM",
        "CKG_TIME_NM",
    ]
]

# '분이내' 문자열 제거
recipe_df["CKG_TIME_NM"] = (
    recipe_df["CKG_TIME_NM"].astype(str).str.replace("분이내", "", regex=False)
)

# 요리명 리스트
cooking_df = recipe_df[["CKG_NM"]].drop_duplicates().reset_index(drop=True)
result_dict = cooking_df.to_dict(orient="index")
result_dict = {k: v["CKG_NM"] for k, v in result_dict.items()}
result_json = json.dumps(result_dict, ensure_ascii=False)
with open("Data/result/cooking_list.json", "w", encoding="utf-8") as f:
    f.write(result_json)

# 요리 방법 리스트
cooking_df = recipe_df[["CKG_MTH_ACTO_NM"]].drop_duplicates().reset_index(drop=True)
result_dict = cooking_df.to_dict(orient="index")
result_dict = {k: v["CKG_MTH_ACTO_NM"] for k, v in result_dict.items()}
result_json = json.dumps(result_dict, ensure_ascii=False)
with open("Data/result/cooking_methods_list.json", "w", encoding="utf-8") as f:
    f.write(result_json)

# 요리 상황 리스트
cooking_df = recipe_df[["CKG_STA_ACTO_NM"]].drop_duplicates().reset_index(drop=True)
result_dict = cooking_df.to_dict(orient="index")
result_dict = {k: v["CKG_STA_ACTO_NM"] for k, v in result_dict.items()}
result_json = json.dumps(result_dict, ensure_ascii=False)
with open("Data/result/cooking_situation_list.json", "w", encoding="utf-8") as f:
    f.write(result_json)

# 요리 메인재료 리스트
cooking_df = recipe_df[["CKG_MTRL_ACTO_NM"]].drop_duplicates().reset_index(drop=True)
result_dict = cooking_df.to_dict(orient="index")
result_dict = {k: v["CKG_MTRL_ACTO_NM"] for k, v in result_dict.items()}
result_json = json.dumps(result_dict, ensure_ascii=False)
with open("Data/result/cooking_main_ingredients_list.json", "w", encoding="utf-8") as f:
    f.write(result_json)

# 요리 종류 리스트
cooking_df = recipe_df[["CKG_KND_ACTO_NM"]].drop_duplicates().reset_index(drop=True)
result_dict = cooking_df.to_dict(orient="index")
result_dict = {k: v["CKG_KND_ACTO_NM"] for k, v in result_dict.items()}
result_json = json.dumps(result_dict, ensure_ascii=False)
with open("Data/result/cooking_type_list.json", "w", encoding="utf-8") as f:
    f.write(result_json)
