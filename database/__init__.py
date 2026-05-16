# database/__init__.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["plantdb"]  # 👈 Ye hi db hai jisko import karna hai
