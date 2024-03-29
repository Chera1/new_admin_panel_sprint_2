import abc
import json
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""


class JsonFileStorage(BaseStorage):
    """Класс для работы с сохранением и загрузкой данных в JSON формате."""
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, 'r') as f:
                try:
                    data = json.load(f)

                    return data
                except:
                    return dict()
        except FileNotFoundError:
            return dict()

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as f:
            data = json.dumps(state)
            f.write(data)


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        data = dict()
        if key:
            data[key] = value
            self.storage.save_state(data)
        else:
            return None

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state()
        if state.get(key, False):
            return state[key]
        else:
            return None


def get_status(filepath):
    """Функция, отвечающая за создание состояния и сохраняющая данные в переданный файл.

    :param filepath: Путь к файлу

    :return: текущее состояние"""
    storage = JsonFileStorage(filepath)
    state = State(storage)
    return state
