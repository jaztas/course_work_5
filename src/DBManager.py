import psycopg2


class DBManager:
	""" Клас для взаимодействия с базой данных. """

	def __init__(self, database_name, params) -> None:
		""" Инициализируем подключение к базе данных. """
		self.conn = psycopg2.connect(dbname=database_name, **params)

	@staticmethod
	def create_database(params: dict, database_name) -> None:
		""" Создает базу данных. """
		conn = psycopg2.connect(dbname='postgres', **params)
		conn.autocommit = True
		cur = conn.cursor()
		cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
		cur.execute(f'CREATE DATABASE {database_name}')
		conn.close()

	def create_table_employers(self) -> None:
		""" Создает таблицу для компаний. """
		with self.conn.cursor() as cur:
			cur.execute("""
			CREATE TABLE employers (
			company_id SERIAL PRIMARY KEY,
			employer_name VARCHAR UNIQUE
			)
			""")
		self.conn.commit()

	def create_table_vacancy(self) -> None:
		""" Создает таблицу для вакансий. """
		with self.conn.cursor() as cur:
			cur.execute("""
			CREATE TABLE vacancies (
			vacancy_id serial,
			vacancy_name text not null,
			salary int,
			company_name text REFERENCES employers(employer_name) NOT NULL,
			vacancy_url varchar not null,
			foreign key(company_name) references employers(employer_name)
			)
			""")
		self.conn.commit()

	def add_employer_in_bd(self, employers_dict: dict) -> None:
		"""Заполнение таблицы данными компаний в БД. """
		cur = self.conn.cursor()
		for employer in employers_dict:
			cur.execute(
				f"INSERT INTO employers (employer_name) VALUES ('{employer}')")
		self.conn.commit()

	def add_vacancy_in_bd(self, employers_all_vacancies: list) -> None:
		"""Заполнение таблицы данными вакансий в БД."""
		cur = self.conn.cursor()
		for vacancy in employers_all_vacancies:
			cur.execute(
				f"INSERT INTO vacancies(vacancy_name, salary, company_name, vacancy_url) values "
				f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
				f"'{vacancy['employer']}', '{vacancy['url']}')")
		self.conn.commit()

	def get_companies_and_vacancies_count(self) -> list:
		""" Получает список всех компаний и количество вакансий у каждой компании. """
		with self.conn.cursor() as cur:
			cur.execute('SELECT company_name, COUNT(vacancy_name) from vacancies GROUP BY company_name')
			answer = cur.fetchall()
		return answer

	def get_all_vacancies(self) -> list:
		""" Получает список всех вакансий с указанием названия компании,
		названия вакансии и зарплаты и ссылки на вакансию. """
		with self.conn.cursor() as cur:
			cur.execute('SELECT * FROM  vacancies')
			answer = cur.fetchall()
		return answer

	def get_avg_salary(self) -> list:
		""" Получает среднюю зарплату по вакансиям. """
		with self.conn.cursor() as cur:
			cur.execute('SELECT AVG(salary) FROM  vacancies')
			answer = cur.fetchall()
		return answer

	def get_vacancies_with_higher_salary(self) -> list:
		""" Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """
		with self.conn.cursor() as cur:
			cur.execute('SELECT * FROM  vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)')
			answer = cur.fetchall()
		return answer

	def get_vacancies_with_keyword(self, word) -> list:
		"""  Получает список всех вакансий, в названии которых содержатся ключевые слова, например python """
		with self.conn.cursor() as cur:
			cur.execute(f"SELECT * FROM  vacancies WHERE vacancy_name LIKE '%{word}%'")
			answer = cur.fetchall()
		return answer

	def quit(self) -> None:
		""" Закрывает соединение базой данных. """
		self.conn.close()
