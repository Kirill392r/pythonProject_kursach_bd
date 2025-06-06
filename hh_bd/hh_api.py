from typing import Any, Dict, List

import requests


class HHParser:
    """Класс получения работодателей и их вакансий"""

    def __init__(self) -> None:
        """Получение url работодателей и вакансий"""
        self.__url_employers: str = "https://api.hh.ru/employers"
        self.__url_vacancies: str = "https://api.hh.ru/vacancies"

    def get_employers(self) -> List[Dict[str, str]]:
        """Получение id и name работодателей"""
        params: Dict[str, Any] = {"sort_by": "by_vacancies_open", "per_page": 10}
        response = requests.get(self.__url_employers, params=params)
        response.raise_for_status()
        employers = response.json()["items"]
        return [
            {"id": employer["id"], "name": employer["name"]} for employer in employers
        ]

    def get_vacancies_by_employer(self, employer_id: str) -> List[Dict[str, Any]]:
        """Получение вакансий работодателя"""
        params: Dict[str, Any] = {"employer_id": employer_id, "per_page": 100}
        response = requests.get(self.__url_vacancies, params=params)
        response.raise_for_status()
        vacancies = response.json()["items"]
        return vacancies

    def get_all_vacancies_by_employers(self) -> List[Dict[str, Any]]:
        """Получение всех вакансий работодателей"""
        employers = self.get_employers()
        all_vacancies: List[Dict[str, Any]] = []
        for employer in employers:
            vacancies = self.get_vacancies_by_employer(employer["id"])
            for vacancy in vacancies:
                vac = self.filter_vacancy(vacancy)
                vac["employer_id"] = employer["id"]
                all_vacancies.append(vac)
        return all_vacancies

    @staticmethod
    def filter_vacancy(vacancy: Dict[str, Any]) -> Dict[str, Any]:
        """Фильтр для вакансий"""
        if vacancy.get("salary"):
            salary_from = vacancy["salary"].get("from", 0)
            salary_to = vacancy["salary"].get("to", 0)
        else:
            salary_from = 0
            salary_to = 0
        return {
            "id": vacancy["id"],
            "name": vacancy["name"],
            "area": vacancy["area"]["name"],
            "url": vacancy["alternate_url"],
            "salary_from": salary_from,
            "salary_to": salary_to,
        }
