from typing import Any

import psycopg2

from hh_bd.config import config


class DBManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.params = config()

    def connect(self) -> Any:
        """Создание подключения к базе данных."""
        return psycopg2.connect(dbname=self.db_name, **self.params)

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, COUNT(v.id)
                    FROM employers e
                    LEFT JOIN vacancies v ON e.id = v.employer_id
                    GROUP BY e.name
                    ORDER BY COUNT(v.id) DESC;
                """
                )
                return cur.fetchall()

    def get_all_vacancies(self) -> list[tuple]:
        """Получает список всех вакансий с названием компании, вакансии, зарплатой и ссылкой."""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name AS employer, v.name, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    ORDER BY e.name;
                """
                )
                return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям."""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT AVG(
                        (COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0
                    )
                    FROM vacancies
                    WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
                """
                )
                avg_salary = cur.fetchone()[0]
                return round(avg_salary, 2) if avg_salary else 0.0

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Получает вакансии с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name AS employer, v.name, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE ((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0) > %s;
                """,
                    (avg_salary,),
                )
                return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Получает вакансии, содержащие ключевое слово в названии."""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name AS employer, v.name, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE LOWER(v.name) LIKE %s;
                """,
                    (f"%{keyword.lower()}%",),
                )
                return cur.fetchall()
