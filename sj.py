from abc import abstractmethod, ABC
import os
from datetime import datetime
import requests
import json
import time

class SJ():
    '''Класс для работы с API SuperJob.'''
    url = f'https://api.superjob.ru/2.0/vacancies/'
    sj_api_secret_key = os.getenv('SJ_API_SECRET_KEY')

    def __init__(self, keyword):
        self.keyword = keyword
        self.headers = {'X-Api-App-Id': self.sj_api_secret_key}
        self.params = {'keyword': self.keyword, 'page': 0, 'count': 100}
        self.vacancies = []


    def get_vacancies(self) -> None:
        """
        Функция получает вакансии по заданным параметрам, используя API запросы к серверу.
        Загружает страницы с вакансиями, пока не загрузит ВСЕ страницы с вакансиями. Затем фильтрует полученный список вакансий
        по заданным условиям, используя метод filter_vacancy().
         Наконец, отфильтрованные вакансии добавляются в список self.vacancies. Функция возвращает None.
        """

        vacancies_tmp = []
        while True:
            url = f'https://api.superjob.ru/2.0/vacancies/'
            response = requests.get(url, headers=self.headers, params=self.params)
            if response.status_code == 200:
                print(f'{self.__class__.__name__} загрузка страницы {self.params["page"]}')
                data = response.json()
                vacancies_tmp.extend(data['objects'])
                more_results = data['more']
                if not more_results:
                    break
                self.params['page'] += 1
            else:
                print('Ошибка при получении списка вакансий с API SuperJob.ru:', response.text)
        filtered_vacancies = self.filter_vacancy(vacancies_tmp)
        self.vacancies.extend(filtered_vacancies)

    @staticmethod
    def filter_vacancy(vacancy_data: list) -> list:
        """
        Функция извлекает и конвертирует данные о вакансиях.

        """
        vacancies = []
        for vacancy in vacancy_data:
            if not vacancy["is_closed"]:
                datetime_obj = datetime.fromtimestamp(vacancy['date_published'])
                formatted_date = datetime_obj.strftime("%Y.%m.%d %H:%M:%S")
                payment_from = vacancy['payment_from'] if vacancy['payment_from'] is not None else 0
                payment_to = vacancy['payment_to'] if vacancy['payment_to'] is not None else 0
                processed_vacancy = {
                    'platform': "SuperJob",
                    "id": vacancy["id"],
                    'title': vacancy['profession'],
                    'company': vacancy['firm_name'],
                    'url': vacancy['link'],
                    'area': vacancy['town']['title'],
                    'address': vacancy['address'],
                    'candidat': vacancy['candidat'],
                    'vacancyRichText': vacancy['vacancyRichText'],
                    'date_published': formatted_date,
                    'payment': {'from': payment_from, 'to': payment_to, 'currency': vacancy["currency"]}
                }
                vacancies.append(processed_vacancy)

        return vacancies







