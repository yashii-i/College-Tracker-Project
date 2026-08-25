import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import json

def route_request(prompt, out_of_state_url=None):
    prompt_lower = prompt.lower()
    uc_keywords = ["uc", "university of california,", "berkeley", "California", "davis"]
    is_a_uc = any(keyword in prompt_lower for keyword in uc_keywords )

    if is_a_uc:
        with open("uc_college_knowledge_base.txt", "r", encoding="utf-8") as file:
            knowledge_base = file.read()
        url_match = re.search(r"https://[^\s]+", knowledge_base)

        if url_match:
            uc_url = url_match.group(0)
            headers = {"User Agent": "Mozilla/5.0"}
            response = requests.get(uc_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            for element in soup:
                element.decompose(["script", "style", "nav","header","footer"])
                clean_text = soup.get_text(separator="") 
                return re.sub(r'\s+', '',clean_text()).strip()
        return knowledge_base
    
    else:
        if out_of_state_url:
            headers = {"User Agent": "Mozilla/5.0"}
            response = requests.get(out_of_state_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            for element in soup:
                element.decompose(["script", "style", "nav","header","footer"])
                flat_text = soup.get_text(separator="") 
                return re.sub(r'\s+', '',flat_text()).strip()
            return flat_text
        return ""
    
