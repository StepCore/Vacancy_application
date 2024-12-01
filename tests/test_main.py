from main import main
from src.api_settings import HH


def test_vacancy(vacancy_112238167, vacancy_street):
    assert HH().load_vacancies('112238167') == vacancy_112238167
    assert HH().load_vacancies('Пермякова') == vacancy_street
