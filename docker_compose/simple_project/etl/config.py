import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class Settings(BaseSettings):
    """Класс, хранящий настройки приложения."""
    pg_dsn: PostgresDsn = 'postgres://{user}:{password}@{host}:{port}/{dbname}'.format(user=os.environ.get('DB_USER'),
                                                                                       password=os.environ.get(
                                                                                           'DB_PASSWORD'),
                                                                                       host=os.environ.get('HOST'),
                                                                                       port=os.environ.get('PORT'),
                                                                                       dbname=os.environ.get('DB_NAME'))
