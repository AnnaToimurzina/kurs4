from hh import Vacancy, HH
from sj import SJ
from json_class import JsonJobFile
from Error_pars import JobParseXNoObjectError

class Page1:
    """
    Класс для взаимодействия с пользователем. Главная страница
    """
    __slots__ = ("apis", "data", "path")

    def __init__(self) -> None:
        self.apis = [HH, SJ]
        self.data = []
        self.path = [JsonJobFile]

    def __call__(self) -> None:
        while True:
            print("Программа для поиска и подбора вакансий к платформам SuperJob и HeadHunter\n", "_" * 60)
            print("Введите команду:\n"
                  "1. - запрос к платформе SuperJob\n"
                  "2. - запрос к платформе HeadHunter\n"
                  "3. - запрос ко всем платформам\n"
                  "0. - назад")
            try:
                command = int(input().strip())
                if command == 1:
                    keyword = input("Введите поисковый запрос: ")
                    self.search_vacancies(self.apis[0](keyword=keyword))
                elif command == 2:
                    keyword = input("Введите поисковый запрос: ")
                    self.search_vacancies(self.apis[1](keyword=keyword))
                elif command == 3:
                    keyword = input("Введите поисковый запрос: ")
                    for api in self.apis:
                        self.search_vacancies(api(keyword=keyword))
                elif command == 0:
                    return
                else:
                    raise ValueError
            except ValueError:
                print("Недопустимая команда")

    def search_vacancies(self, api: object) -> None:
        """
        Функция для получения вакансий от api
        """
        api.get_vacancies()
        vacancies = api.vacancies
        self.data.clear()

        self.data.extend(vacancies)

        if len(self.data) > 0:
            print("Вакансии успешно загружены\n")
        else:
            print("Вакансия не найдена. Повторите запрос")


if __name__ == "__main__":
    Page1()()


