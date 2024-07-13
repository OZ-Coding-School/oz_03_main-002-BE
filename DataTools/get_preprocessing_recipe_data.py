import json
import os

import pandas as pd

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

# URL 접두사 추가
url_prefix = "https://m.10000recipe.com/recipe/"
recipe_df["RCP_SNO"] = url_prefix + recipe_df["RCP_SNO"].astype(str)


recipe_df = recipe_df.rename(
    columns={
        "RCP_SNO": "URL",
        "RCP_TTL": "recipe_name",
        "CKG_NM": "cooking_name",
        "RGTR_NM": "nickname",
        "INQ_CNT": "recommand_num",
        "CKG_MTH_ACTO_NM": "cooking_method",
        "CKG_STA_ACTO_NM": "situation_type",
        "CKG_MTRL_ACTO_NM": "main_ingredient_type",
        "CKG_KND_ACTO_NM": "cooking_type",
        "CKG_IPDC": "recipe_intro",
        "CKG_INBUN_NM": "eat_people",
        "CKG_DODF_NM": "difficulty",
        "CKG_TIME_NM": "cooking_time",
    }
)


recipe_df["thumbnail_url"] = None
recipe_df["ingre_list"] = None
recipe_df["detail_recipes"] = None
recipe_df["detail_pics"] = None
recipe_df["detail_tips"] = None


os.makedirs("../Scraping/Data", exist_ok=True)

recipe_dict = recipe_df.to_dict("index")
result_json = json.dumps(recipe_dict, ensure_ascii=False)

with open("../Scraping/Data/preprocessed_data.json", "w") as f:
    f.write(result_json)
