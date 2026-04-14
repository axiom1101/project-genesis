from pathlib import Path
import sys

from qdrant_client import QdrantClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.storage.db import PostgresManager

def test_postgres():
    print("Проверка подключения к PostgreSQL...")
    db_manager = PostgresManager()

    try:
        result = db_manager.fetch_query("SELECT version();")
        if result:
            print(f"✅ Успех! Версия БД: {result[0][0]}\n")
        else:
            print("❌ Не удалось получить версию БД.\n")
    except Exception as e:
        print(f"❌ Ошибка подключения к Postgres: {e}\n")
    finally:
        db_manager.close()

def test_qdrant():
    print("Проверка подключения к Qdrant...")
    try:
        client = QdrantClient(url="http://localhost:6333")
        collections = client.get_collections()
        print(f"✅ Успех! Qdrant доступен. Коллекции: {collections.collections}\n")
    except Exception as e:
        print(f"❌ Ошибка подключения к Qdrant: {e}\n")

if __name__ == "__main__":
    print("=== СТАРТ ПРОВЕРКИ ИНФРАСТРУКТУРЫ ===\n")
    test_postgres()
    test_qdrant()