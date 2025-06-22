import os
from dotenv import load_dotenv

load_dotenv()

API_NAME = "Snap2Report API"
API_KEY = os.getenv('API_KEY')

GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
# GROQ_MODEL = "llama-3.3-70b-versatile"
# GROQ_MODEL = "qwen-qwq-32b"
# GROQ_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

MOONDREAM_API_KEY = os.getenv('MOONDREAM_API_KEY')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
TABLE_NAME = os.getenv('TABLE_NAME')
