from abc import abstractmethod, ABC
from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup
import fake_useragent
import time
class Vacancy(ABC):
    def __init__(self, search_text):
        self.search_text = search_text

    @abstractmethod
    def get_vacancies(self):
        pass

    @staticmethod
    @abstractmethod
    def get_vacancy_info(vacancy):
        pass

    def get_all_vacancies_info(self):
        all_vacancies_info = []
        for vacancy in self.get_vacancies():
            vacancy_info = self.get_vacancy_info(vacancy)
            all_vacancies_info.append(vacancy_info)
        return all_vacancies_info

class HH:
    def __init__(self, search_text):
        self.search_text = search_text


    def get_vacancies(self):
        url = f'https://api.hh.ru/vacancies?text={self.search_text}&page=20'
        response = requests.get(url)
        return response.json()['items']

    @staticmethod
    def get_vacancy_info(vacancy):
        info = {}
        info['name'] = vacancy['name']
        info['salary'] = vacancy['salary'] if vacancy['salary'] else 'Not specified'
        info['skills'] = vacancy['snippet']['requirement'] if vacancy['snippet'] else 'Not specified'
        return info

    def get_all_vacancies_info(self):
        all_vacancies_info = []
        for vacancy in self.get_vacancies():
            vacancy_info = self.get_vacancy_info(vacancy)
            all_vacancies_info.append(vacancy_info)
        return all_vacancies_info



vacancy = HH('Python разработчик')
all_vacancies_info = vacancy.get_all_vacancies_info()
print(all_vacancies_info)

