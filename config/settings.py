import os
from dotenv import load_dotenv

load_dotenv()

LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')
LLAMA_API_URL = os.getenv('LLAMA_API_URL')
