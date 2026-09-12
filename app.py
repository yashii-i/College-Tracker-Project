import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
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
    
def extract_data(text_content):
    pattern = (
        r"Name:\s*(?P<name>[A-Za-z ]+).*?"
        r"Location:\s*(?P<location>[A-Za-z ]+).*?"
        r"Class Size:\s*(?P<class_size>[0-9,]+).*?"
        r"Rank:\s*(?P<rank>[0-9,]+).*?"
        r"# of Majors:\s(?P<majors>[0-9,]+).*?"
        r"Graduation Rate:\s(?P<grad_rate>[0-9,]\%+).*?"
        r"Average Tuition:\s*(?P<avg_tuition>\$[0-9,]+).*?"
        r"In state:\s*(?P<in_state>\$[0-9,]+).*?"
        r"Out of State:\s*(?P<out_state>\$[0-9,]+).*?"
        r"Housing:\s*(?P<housing>\$[0-9,]+).*?"
        r"Application Fee:\s*(?P<app_fee>\$[0-9,]+).*?"
        r"Financial Aid Rate:\s*(?P<financial_aid>[0-9,]\%+).*?"
    
    )
    for match in re.finditer(pattern, text_content):
        data_dict = match.groupdict()
        return data_dict
    