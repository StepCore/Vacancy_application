import json
from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    """Абстрактный класс для работы с API сервиса вакансий."""

    @abstractmethod
    def load_vacancies(self, keyword):
        """Метод для загрузки вакансий по ключевому слову."""
        pass


class HH(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"page": 0, "per_page": 100}
        self.vacancies = []
        super().__init__()

    def load_vacancies(self, keywords):
        """Основная функция для фильтрации вакансий"""
        self.__params["page"] = 0
        while self.__params.get("page") < 20:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            vacancies = response.json()["items"]
            for vacancy in vacancies:
                if any(
                    keyword.lower() in str(vacancy).lower()
                    for keyword in keywords.split(" ")
                ):
                    self.vacancies.append(vacancy)
            self.__params["page"] += 1
        return self.vacancies


class FileSaverToJSON:
    """Класс для сохранения данных в формате JSON."""

    def __init__(self, file_path='default.json'):
        self.__file_path = file_path

    def save(self, data):
        """Метод для сохранения данных в файл."""
        with open(self.__file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def load(self):
        """Вспомогательная функция для топа вакансий"""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Файл не найден. Убедитесь, что вы сначала сохранили вакансии.")
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения файла. Убедитесь, что файл содержит корректный JSON.")
            return []


def get_top_n_vacancies(file_saver, top_n):
    """Функция сортирующая топ вакансий"""
    vacancies = file_saver.load()

    def get_salary(vacancy):
        try:
            salary = vacancy.get("salary").get("from")
        except Exception:
            return 0
        if isinstance(salary, (int, float)):
            return salary
        return 0

    top_vacancies = sorted(vacancies, key=get_salary, reverse=True)[:top_n]
    return top_vacancies


# vacancies = HH().load_vacancies("your_text")

# print(*vacancies, sep='\n')
