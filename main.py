from hh_bd.class_DBManager import DBManager
from hh_bd.create_bd import (create_database, create_tables,
                             insert_data_in_tables)


def main():
    db_name = "test_db"

    create_database(db_name)
    create_tables(db_name)
    insert_data_in_tables(db_name)

    db = DBManager(db_name)

    while True:
        print("\nВыберите действие:")
        print("1. Компании и число вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с ЗП выше средней")
        print("5. Поиск по ключевому слову")
        print("0. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            data = db.get_companies_and_vacancies_count()
            for company, count in data:
                print(f"{company}: {count} вакансий")

        elif choice == "2":
            data = db.get_all_vacancies()
            for employer, name, salary_from, salary_to, url in data:
                print(
                    f"{employer} | {name} | от {salary_from or '-'} до {salary_to or '-'} | {url}"
                )

        elif choice == "3":
            avg = db.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg} руб.")

        elif choice == "4":
            data = db.get_vacancies_with_higher_salary()
            for employer, name, salary_from, salary_to, url in data:
                print(
                    f"{employer} | {name} | от {salary_from or '-'} до {salary_to or '-'} | {url}"
                )

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ").strip()
            data = db.get_vacancies_with_keyword(keyword)
            for employer, name, salary_from, salary_to, url in data:
                print(
                    f"{employer} | {name} | от {salary_from or '-'} до {salary_to or '-'} | {url}"
                )

        elif choice == "0":
            print("Завершение программы.")
            break

        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
