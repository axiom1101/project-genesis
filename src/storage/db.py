import os
from typing import Any

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as PgConnection
from psycopg2.extensions import cursor as PgCursor


class PostgresManager:
    """Manage PostgreSQL connection and raw SQL queries."""

    def __init__(self) -> None:
        """Initialize PostgreSQL connection and cursor from .env values."""
        load_dotenv()
        self.conn: PgConnection | None = None
        self.cursor: PgCursor | None = None

        try:
            self.conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=os.getenv("POSTGRES_PORT", "5432"),
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
            )
            self.cursor = self.conn.cursor()
        except Exception as error:
            print(f"[PostgresManager.__init__] Connection error: {error}")

        # Ensure database schema exists on every connection.
        self.init_tables()

    def execute_query(self, query: str, params: tuple[Any, ...] | None = None) -> None:
        """Execute INSERT/UPDATE/DELETE query and commit transaction."""
        if self.conn is None or self.cursor is None:
            print("[PostgresManager.execute_query] Connection is not initialized.")
            return

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as error:
            self.conn.rollback()
            print(f"[PostgresManager.execute_query] Query execution error: {error}")

    def fetch_query(
        self, query: str, params: tuple[Any, ...] | None = None
    ) -> list[tuple[Any, ...]]:
        """Execute SELECT query and return all rows."""
        if self.cursor is None:
            print("[PostgresManager.fetch_query] Connection is not initialized.")
            return []

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as error:
            print(f"[PostgresManager.fetch_query] Query fetch error: {error}")
            return []

    def add_user(self, telegram_id: int) -> int | None:
        """Create user by telegram_id and return internal user id."""
        insert_sql = """
        INSERT INTO users (telegram_id)
        VALUES (%s)
        ON CONFLICT (telegram_id) DO NOTHING
        RETURNING id;
        """
        inserted_rows = self.fetch_query(insert_sql, (telegram_id,))
        if inserted_rows:
            return inserted_rows[0][0]

        select_sql = "SELECT id FROM users WHERE telegram_id = %s;"
        existing_rows = self.fetch_query(select_sql, (telegram_id,))
        if existing_rows:
            return existing_rows[0][0]

        return None

    def add_chat_message(self, user_id: int, role: str, content: str) -> None:
        """Save one chat message for a specific user."""
        query = """
        INSERT INTO chat_history (user_id, role, content)
        VALUES (%s, %s, %s);
        """
        self.execute_query(query, (user_id, role, content))

    def get_chat_history(self, user_id: int, limit: int = 10) -> list[dict[str, str]]:
        """Return chat history as LLM-friendly list of role/content dictionaries."""
        query = """
        SELECT role, content
        FROM chat_history
        WHERE user_id = %s
        ORDER BY created_at ASC
        LIMIT %s;
        """
        rows = self.fetch_query(query, (user_id, limit))
        return [{"role": role, "content": content} for role, content in rows]

    def close(self) -> None:
        """Close cursor and database connection."""
        try:
            if self.cursor is not None:
                self.cursor.close()
                self.cursor = None
            if self.conn is not None:
                self.conn.close()
                self.conn = None
        except Exception as error:
            print(f"[PostgresManager.close] Close error: {error}")

    def init_tables(self) -> None:
        """Create required tables if they do not exist."""
        users_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        chat_history_table_sql = """
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            role VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Use the existing error handling + transaction logic from execute_query().
        self.execute_query(users_table_sql)
        self.execute_query(chat_history_table_sql)