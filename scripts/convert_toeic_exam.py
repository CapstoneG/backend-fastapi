import json
import pymongo

with open('scripts/toeic_exam/224.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data.sort(key=lambda x: int(x['question_number']))

def get_part_number(q_number):
    n = int(q_number)
    if 1 <= n <= 6:
        return 'Part1'
    if 7 <= n <= 31:
        return 'Part2'
    if 32 <= n <= 69:
        return 'Part3'
    if 70 <= n <= 100:
        return 'Part4'
    if 101 <= n <= 130:
        return 'Part5'
    if 131 <= n <= 146:
        return 'Part6'
    if 147 <= n <= 200:
        return 'Part7'
    return 'UnknownPart'

structured_data = {
    "exam_title": "TOEIC Exam 224",
    "parts": {f"Part{i}": [] for i in range(1, 8)}
}

current_group = None
last_criteria = None
last_part = None

for q in data:
    q_num = q['question_number']
    part_name = get_part_number(q_num)

    criteria = None
    if part_name in ['Part1', 'Part2', 'Part3', 'Part4']:
        criteria = q['audio_url']
    elif part_name in ['Part6', 'Part7']:
        criteria = q['reading_text']
    else:
        criteria = q_num

    if part_name != last_part or criteria != last_criteria:
        new_group = {
            "group_content": {},
            "questions": []
        }

        new_group["group_content"]["audio_url"] = q['audio_url'] or ''
        new_group["group_content"]["reading_text"] = q['reading_text'] or ''
        new_group["group_content"]["reading_text_clean"] = q['reading_text_clean'] or ''
        new_group["group_content"]["image_url"] = q["image_url"] or []

        structured_data["parts"][part_name].append(new_group)
        current_group = new_group

        last_criteria = criteria
        last_part = part_name

    current_group["questions"].append(q)



with open('scripts/toeic_exam_structured/224_structured.json', 'w', encoding='utf-8') as f:
    json.dump(structured_data, f, ensure_ascii=False, indent=2)    

import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "EnglishApp")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
exams_collection = db["toeic_exams"]

try:
    exams_collection.insert_one(structured_data)
    print("Data inserted successfully")
except Exception as e:
    print(f"An error occurred: {e}")