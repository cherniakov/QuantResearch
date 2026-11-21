
import os
from dotenv import load_dotenv
from MOEXPy import MOEXPy

load_dotenv()

token = os.getenv("MOEX_API_TOKEN")

if not token:
    raise ValueError("MOEX_API_TOKEN не найден в .env")

mp_provider = MOEXPy(token)

print("Токен успешно загружен и, возможно, сохранен в систему.")

