from hh import HH
from sj import SJ
from json_class import JsonJobFile
from vacancy import Vacancy

def user_interaction():
    apis = [HH, SJ]
    data = []
    path = [JsonJobFile]

    print("Программа для поиска и подбора вакансий к платформам SuperJob и HeadHunter\n", "_" * 60)
    print("Введите команду:\n"
          "1. - запрос к платформе HeadHunter\n"
          "2. - запрос к платформе Superjob\n"
          "3. - запрос ко всем платформам\n"
          "0. - назад")

    try:
        command = int(input().strip())

        if command == 1:
            keyword = input("Введите поисковый запрос: ")
            search_vacancies(apis[0](keyword=keyword), data)
        elif command == 2:
            keyword = input("Введите поисковый запрос: ")
            search_vacancies(apis[1](keyword=keyword), data)
        elif command == 3:
            keyword = input("Введите поисковый запрос: ")
            for api in apis:
                search_vacancies(api(keyword=keyword), data)
        elif command == 0:
            return
        else:
            raise ValueError

    except ValueError:
        print("Недопустимая команда")

    json_save = JsonJobFile()
    json_save.write_file(data)
    vacancies = json_save.get_vacancies()

    for vacancy in vacancies:
        print(vacancy)
        print("-" * 100)

    print("Выберите дальнейшие действия:")
    print("1: Вывод вакансий отсортированных по ЗП")
    print("2: Вывод вакансий по городу")

    try:
        answer = int(input())
        if answer == 1:
            vacancies.sort()
            first(vacancies)

        elif answer == 2:
            city = input("Введите город поиска").title()
            vacancies = Vacancy.vacancis_by_city(vacancies, city)
            first(vacancies)
        elif answer == 0:
            return
        else:
            raise ValueError

    except ValueError:
        print("Недопустимая команда")


def first(vacancies):
    for vacancy in vacancies:
        print(vacancy)
        print("-" * 100)

def search_vacancies(api, data):
    """
    Функция для получения вакансий от api
    """
    api.get_vacancies()
    vacancies = api.vacancies
    data.extend(vacancies)


    if len(data) > 0:
        print("Вакансии успешно загружены\n")
    else:
        print("Вакансия не найдена. Повторите запрос")


if __name__ == "__main__":
    user_interaction()

