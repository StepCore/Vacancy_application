from src.api_settings import HH, FileSaverToJSON, get_top_n_vacancies


def main():
    """Запуск программы"""
    file_saver = FileSaverToJSON(r'./data/vacancies.json')

    while True:
        print('1. Поиск вакансий на hh.ru\n'
              '2. Вывести топ вакансий по зарплате\n'
              '3. Поиск вакансии по ключевому слову в описании\n'
              '4. Завершить программу')

        user_choice = input('Введите число: ')
        if user_choice == '1':
            search_query = input('Введите название вакансии: ')
            vacancies = HH().load_vacancies(search_query)
            file_saver.save(vacancies)
            print(f'Найдено {len(vacancies)} вакансий и сохранено в файл "vacancies.json"')
            break

        elif user_choice == '2':
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            top_vacancies = get_top_n_vacancies(file_saver, top_n)
            print(f'Топ {top_n} вакансий по зарплате:')
            for vacancy in top_vacancies:
                print(vacancy)
            break

        elif user_choice == '3':
            keywords = input("Введите ключевые слова для фильтрации вакансий: ")
            vacancies = HH().load_vacancies(keywords)
            print(*vacancies, sep='\n')
            break

        elif user_choice == '4':
            print('Программа завершена')
            break

        else:
            print('Пожалуйста, введите число от 1 до 4')


# main()
