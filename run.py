from src.main import main, monitoring_task, bot
import asyncio
import logging
import sys
from pathlib import Path

# Добавляем путь к src в PYTHONPATH
sys.path.append(str(Path(__file__).parent))


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


async def startup():
    try:
        monitoring = asyncio.create_task(monitoring_task())
        await main()
    except KeyboardInterrupt:
        logger.info("Получен сигнал завершения работы")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(startup())
    except KeyboardInterrupt:
        pass
