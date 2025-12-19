import json
import os
from time import sleep
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

import cloudinary
import cloudinary.uploader
from gtts import gTTS

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "EnglishApp")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "Sentences")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

datasets = []

with open('scripts/datasets.json', 'r', encoding='utf-8') as f:
    datasets = json.load(f)

def process_data(data_list):
    processed_count = 0
    total = len(data_list)

    print(f"Total records to process: {total}")

    for data in data_list:
        try:
            tts = gTTS(text=data['text'], lang='en', slow=False)

            temp_audio_file = f"{data['id']}.mp3"
            tts.save(temp_audio_file)

            print(f"Uploading audio for ID {data['id']} to Cloudinary...")
            upload_result = cloudinary.uploader.upload(
                temp_audio_file, 
                folder="english_app_audio",
                public_id=data['id'],
                resource_type="auto",
            )

            data['audio_url'] = upload_result.get('secure_url', '')
            print(f"Uploaded audio URL: {data['audio_url']}")
            if os.path.exists(temp_audio_file):
                os.remove(temp_audio_file)

            processed_count += 1
            sleep(1)  
        except Exception as e:
            print(f"Error processing ID {data['id']}: {e}")

    return data_list

if __name__ == "__main__":

    # final_data = process_data(datasets)
    # if final_data:
    #     try:
    #         print(f"Inserting {len(final_data)} records into MongoDB...")
    #         insert_result = collection.insert_many(final_data)
    #         print(f"Inserted record IDs: {insert_result.inserted_ids}")
    #     except Exception as e:
    #         print(f"Error inserting records into MongoDB: {e}")
    # else:
    #     print("No data to insert.")

    # client.admin.command('ping')
    # print("Pinged your deployment. You successfully connected to MongoDB!")

    for data in datasets:
        sentence = {
            "id": data['id'],
            "text": data['text'],
            "topic": data['topic'],
            "level": data['level'],
            "audio_url": f"https://res.cloudinary.com/{os.getenv('CLOUDINARY_CLOUD_NAME')}/video/upload/english_app_audio/{data['id']}.mp3"
        }

        try:
            inser_result = collection.insert_one(sentence)
            print(f"Inserted record ID: {inser_result.inserted_id}")
        except Exception as e:
            print(f"Error inserting record ID {data['id']}: {e}")

    