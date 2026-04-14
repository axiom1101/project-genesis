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