import json
import chardet
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Update this path to the correct location of your service account key
service_account_path = "firebase/serviceAccountKey.json"

# Update this path to the correct location of your JSON dataset
json_file = "JSON_Codes/Most_Wickets_Innings.json"

if not os.path.exists(service_account_path):
    print(f"Error: Service account key not found at {service_account_path}")
    exit(1)

if not os.path.exists(json_file):
    print(f"Error: JSON file not found at {json_file}")
    exit(1)

cred = credentials.Certificate(service_account_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

with open(json_file, "rb") as f:
    data_bytes = f.read()

if not data_bytes.strip():
    print("Error: JSON file is empty.")
    exit(1)

detected = chardet.detect(data_bytes)
encoding = detected.get("encoding") or "utf-8"
data_str = data_bytes.decode(encoding, errors="ignore")

try:
    data = json.loads(data_str)
except json.JSONDecodeError as e:
    print(f"JSON Decode Error: {e}")
    exit(1)

if not isinstance(data, list):
    print("Error: JSON file should contain a list of documents.")
    exit(1)

collection_ref = db.collection("Most_Wickets_Innings")
for doc in data:
    if isinstance(doc, dict):
        collection_ref.add(doc)
    else:
        print(f"Skipping invalid document: {doc}")

print("Data upload complete.")
