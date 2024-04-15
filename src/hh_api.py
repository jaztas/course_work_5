import requests


class HeadHunterAPI:
	"""Класс для работы с API HH.ru"""
	database_name = 'new_db'
	employers_dict = {'Яндекс': '1740', 'Ozon': '2180', 'Тинькофф': '78638', 'СБЕР': '3529', 'МегаФон': '3127',
					  'МТС': '3776', 'Tele2': '4219', 'Альфа-Банк': '80', 'Банк ВТБ (ПАО)': '4181', 'Газпромбанк': '3388'}

	@staticmethod
	def get_companies(employer_id) -> dict:
		"""Получение списка компаний. """
		params = {
			"page": 1,
			"per_page": 100,
			"employer_id": employer_id,
			"only_with_salary": True,
			"area": 113,
			"only_with_vacancies": True
		}
		return requests.get("https://api.hh.ru/vacancies", params=params).json()['items']

	def get_vacancies(self) -> list:
		"""Получение списка работодателей"""
		vacancies_list = []
		for employer in self.employers_dict:
			emp_vacancies = self.get_companies(self.employers_dict[employer])
			for vacancy in emp_vacancies:
				if vacancy['salary']['from'] is None:
					salary = 0
				else:
					salary = vacancy['salary']['from']
				vacancies_list.append(
					{'url': vacancy['alternate_url'], 'salary': salary,
					 'vacancy_name': vacancy['name'], 'employer': employer})
		return vacancies_list
