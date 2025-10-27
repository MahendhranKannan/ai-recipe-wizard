from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into os.environ

value = os.getenv("OPENAI_MODEL")
print(value)