import os
from dataclasses import dataclass

@dataclass(frozen=True)
class DBConfig:
    host: str = os.getenv("DB_HOST", "localhost")
    user: str = os.getenv("DB_USER", "root")
    password: str = os.getenv("DB_PASSWORD", "senai110")
    database: str = os.getenv("DB_NAME", "sistema_comercial")

DB = DBConfig()