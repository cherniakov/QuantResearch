# save_token.py
import os
from dotenv import load_dotenv
from FinamPy.FinamPy import FinamPy

load_dotenv()
token = os.getenv('FINAM_TOKEN')
fp_provider = FinamPy(token)
print("Токен успешно загружен и, возможно, сохранен в систему.")
