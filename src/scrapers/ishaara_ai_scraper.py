import requests
import json
import pandas
URL = "https://ishaara.ai/api/words"
HEADERS = {"User-Agent": "Ishara-e-Shikkha RoboFest project (contact: prantotarsrik@gmail.com)"}
resp = requests.get(URL,headers=HEADERS,verify=False)
data = resp.json()
with open("data/raw_words_ishaara_ai.json","w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=2)