from pathlib import Path
import sys

from qdrant_client import QdrantClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.storage.db import PostgresManager
from src.memory.vector_store import QdrantManager

def test_postgres():
    print("Проверка подключения к PostgreSQL...")
    db_manager = PostgresManager()

    try:
        result = db_manager.fetch_query("SELECT version();")
        if result:
            print(f"✅ Успех! Версия БД: {result[0][0]}\n")
        else:
            print("❌ Не удалось получить версию БД.\n")

        # --- ТЕСТ CRUD ОПЕРАЦИЙ ---
        print("Тестируем CRUD операции...")
        
        # 1. Создаем юзера (или получаем существующего)
        test_tg_id = 999888777
        user_id = db_manager.add_user(test_tg_id)
        print(f"👤 Юзер готов! Внутренний ID: {user_id}")
        
        # 2. Пишем историю диалога
        db_manager.add_chat_message(user_id, "user", "Привет, ты кто?")
        db_manager.add_chat_message(user_id, "assistant", "Я ИИ-агент проекта Genesis.")
        print("💬 Сообщения записаны в базу.")
        
        # 3. Читаем историю так, как её будет читать LLM
        history = db_manager.get_chat_history(user_id, limit=5)
        print(f"📜 История диалога: {history}\n")

    except Exception as e:
        print(f"❌ Ошибка подключения к Postgres: {e}\n")
    finally:
        db_manager.close()

def test_qdrant():
    print("Проверка подключения к Qdrant...")
    try:
        qdrant_manager = QdrantManager()
        print("✅ Успех! QdrantManager инициализирован и коллекция проверена/создана.\n")
    except Exception as e:
        print(f"❌ Ошибка Qdrant: {e}\n")

if __name__ == "__main__":
    print("=== СТАРТ ПРОВЕРКИ ИНФРАСТРУКТУРЫ ===\n")
    test_postgres()
    test_qdrant()