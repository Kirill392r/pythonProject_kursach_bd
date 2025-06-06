import psycopg2

from hh_bd.config import config
from hh_bd.hh_api import HHParser


def create_database(name_db: str) -> None:
    """Создание базы данных если её нет, если она существует удаление и её создание"""
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {name_db}")
    cur.execute(f"CREATE DATABASE {name_db}")

    cur.close()
    conn.close()


def create_tables(name_db: str) -> None:
    """Создание таблиц"""
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE employers(
            id int PRIMARY KEY,
            name VARCHAR(255) NOT NULL
            )"""
            )

            cur.execute(
                """CREATE TABLE vacancies(
            id int PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            area VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            salary_from int,
            salary_to int,
            employer_id INT REFERENCES employers(id)
            )"""
            )
    conn.close()


def insert_data_in_tables(name_db: str) -> None:
    """Добавление в таблицы данные"""
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    vacancies = hh_parser.get_all_vacancies_by_employers()
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute(
                    """INSERT INTO employers VALUES(%s, %s)""",
                    (employer["id"], employer["name"]),
                )
            for vacancy in vacancies:
                cur.execute(
                    """INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        vacancy["id"],
                        vacancy["name"],
                        vacancy["area"],
                        vacancy["url"],
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["employer_id"],
                    ),
                )
    conn.close()
