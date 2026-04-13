import os
import psycopg2
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

def test_postgres():
    print("Проверка подключения к PostgreSQL...")
    try:
        # Подключаемся к базе (пока скрипт запущен локально, стучимся на localhost)
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            dbname=os.getenv("POSTGRES_DB")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"✅ Успех! Версия БД: {db_version[0]}\n")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка подключения к Postgres: {e}\n")

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