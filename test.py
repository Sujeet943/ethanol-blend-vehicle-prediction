from dotenv import load_dotenv
import os

loaded = load_dotenv()

print("Loaded:", loaded)
print("Current Folder:", os.getcwd())
print("Key:", os.getenv("GOOGLE_API_KEY"))