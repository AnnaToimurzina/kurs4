from abc import abstractmethod, ABC
from datetime import datetime
import requests

class Abstract_Vacancy(ABC):
    """
    Абстрактный класс для работы с платформами по поиску вакансий по API.
    """
    @abstractmethod
    def get_vacancies(self):
        pass


class HH(Abstract_Vacancy):
    """
    Класс для работы с API HeadHunter.
    """
    def __init__(self, keyword) -> None:
        self.keyword = keyword
        self.base_url = "https://api.hh.ru/vacancies"
        self.vacancies = []

    def get_vacancies(self) -> None:
        """
        Функция возвращает вакансии по параметрам поиска.
        """
        vacancies_tmp = []
        total_pages = 5
        params = {'text': self.keyword, 'page': 0, 'per_page': 20}
        while params["page"] < total_pages:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                print(f'{self.__class__.__name__} загрузка страницы {params["page"]}')
                data = response.json()
                vacancies_tmp.extend(data["items"])
                #total_pages = data['pages']
                params["page"] += 1
            else:
                print('Ошибка при получении списка вакансий с HeadHunter.ru:', response.text)


            '''вызываем метод filter_vacancy() и передаем в него аргумент vacancies_tmp. 
            Затем результат работы этого метода сохраняется в переменную filtered_vacancies.
            Дальше метод extend() добавляет элементы из filtered_vacancies в конец списка self.vacancies.'''
            filtered_vacancies = self.filter_vacancy(vacancies_tmp)
            self.vacancies.extend(filtered_vacancies)

    @staticmethod
    def filter_vacancy(vacancy_data: list) -> list:
        """
        Функция извлекает и конвертирует данные о вакансиях.
        """
        vacancies = []
        for vacancy in vacancy_data:
            if vacancy['type']['id'] == 'open':
                address = vacancy['address']
                address_raw = address['raw'] if address else None
                salary = vacancy['salary']
                if salary:
                    salary_from = salary['from'] if salary['from'] is not None else 0
                    salary_to = salary['to'] if salary['to'] is not None else 0
                    currency = salary['currency'] if salary['currency'] is not None else "RUR"
                else:
                    salary_from = 0
                    salary_to = 0
                    currency = "RUR"
                datetime_obj = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
                formatted_date = datetime_obj.strftime("%Y.%m.%d %H:%M:%S")
                processed_vacancy = {
                    'platform': "HeadHunter",
                    'id': vacancy["id"],
                    'title': vacancy['name'],
                    'company': vacancy['employer']['name'],
                    'url': vacancy['alternate_url'],
                    'area': vacancy['area']['name'],
                    'address': address_raw,
                    'candidat': vacancy['snippet']['requirement'],
                    'vacancyRichText': vacancy['snippet']['responsibility'],
                    'date_published': formatted_date,
                    'payment': {'from': salary_from, 'to': salary_to, 'currency': currency}
                }
                vacancies.append(processed_vacancy)
        return vacancies








