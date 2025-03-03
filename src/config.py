from dotenv import load_dotenv
import os
from pathlib import Path

# Получаем абсолютный путь к корневой директории проекта
BASE_DIR = Path(__file__).parent.parent

# Загружаем .env файл
load_dotenv(BASE_DIR / '.env')

# Получаем и проверяем токен
API_TOKEN = os.getenv('BOT_TOKEN')
if not API_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

# Проверяем формат токена
if not API_TOKEN.count(':') == 1:
    raise ValueError("Неверный формат токена")

CHECK_INTERVAL = 300  # 5 минут в секундах
DB_PATH = BASE_DIR / 'data' / 'monitoring.db'
