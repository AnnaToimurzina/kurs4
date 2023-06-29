import json
import os
from vacancy import Vacancy



class JsonJobFile():
    """
    Класс для работы с вакансиями в json файле.
    """
    def __init__(self) -> None:
        self.file_path = os.path.join('vacancy.json')

    def add_vacancy(self, vacancy, data_append=False) -> None:
        """
        Функция для записи (добавления) вакансий в файл json. Обработаны исключения:
        - файла нет, нет директории с файлом - создаются заново;
        - файл пустой, но функция работает в режиме добавления.
        """
        try:
            if not data_append:
                self.write_file(vacancy)
            else:
                load_data = self.read_file()
                for item in vacancy:
                    load_data.append(item)
                self.write_file(load_data)
        except json.JSONDecodeError:
            self.write_file(vacancy)
        except FileNotFoundError:
            os.makedirs("data")
            self.write_file(vacancy)

    def get_vacancies(self) -> list:
        """
        Функция получения списка экземпляров класса Vacancy.
        """
        vacancies = []
        data = self.read_file()
        for vacancy in data:
            title = vacancy["title"]
            company = vacancy["company"]
            url = vacancy["url"]
            area = vacancy["area"]
            payment_from = vacancy["payment"]["from"]
            payment_to = vacancy["payment"]["to"]
            platform = vacancy["platform"]
            vacancies.append(Vacancy(title, company, url, area, payment_from, payment_to, platform))
        return vacancies

    def remove_vacancy(self, vacancy_id: str) -> None:
        try:
            data = self.read_file()
            data_filtered = [item for item in data if int(item['id']) != int(vacancy_id)]
            self.write_file(data_filtered)
        except ValueError:
            print("id вакансии должно быть числом")
        else:
            print("Вакансия успешно удалена из базы данных")

    def read_file(self):
        """
        Функция чтения данных из файла.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def write_file(self, data):
        """
        Функция записи данных в файл.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def search_in_data(self, data, keywords, result):
        """
        Рекурсивная функция, для поиска во вложенных данных.
        """
        for item in data:
            if isinstance(item, dict):
                for value in item.values():
                    if isinstance(value, (str, float, int)):
                        if any(keyword in str(value).lower() for keyword in keywords):
                            result.append(item)
                            break
                    elif isinstance(value, (dict, list)):
                        self.search_in_data(value, keywords, result)
            elif isinstance(item, list):
                self.search_in_data(item, keywords, result)