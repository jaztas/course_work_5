from src.config import config
from src.hh_api import HeadHunterAPI
from src.DBManager import DBManager


def user_interaction():
	print('Получение данных о вакансиях по API.')
	response = HeadHunterAPI()
	db_name = response.database_name  # Имя для базы данных
	employers_dict = response.employers_dict  # Словарь компаний
	employers_all_vacancies = response.get_vacancies()  # Список вакансий
	params = config()  # Выгружаем параметры
	DBManager.create_database(params, db_name)  # Создаем базу данных
	conn = DBManager(db_name, params)  # Подключение
	DBManager.create_table_employers(conn)  # Создание таблицы компаний
	DBManager.create_table_vacancy(conn)  # Создание таблицы вакансий
	DBManager.add_employer_in_bd(conn, employers_dict)  # Заполнение таблицы компаний
	DBManager.add_vacancy_in_bd(conn, employers_all_vacancies)  # Заполнение таблицы вакансий

	while True:
		user_input = input("""Выберете команду:
							1 - получить список всех компаний и количество их вакансий
							2 - получить список всех вакансий с названием компании, вакансии, зарплаты и ссылку на вакансию
							3 - получить среднюю зарплату по вакансиям
							4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
							5 - получить список всех вакансий, в которых содержатся ключевые слова, например 'python'
							Другие команды завершат программу.\n""")
		if user_input == '1':
			print(DBManager.get_companies_and_vacancies_count(conn))
		elif user_input == '2':
			print(DBManager.get_all_vacancies(conn))
		elif user_input == '3':
			print(DBManager.get_avg_salary(conn))
		elif user_input == '4':
			print(DBManager.get_vacancies_with_higher_salary(conn))
		elif user_input == '5':
			word = input('Введите ключевое слово.\n')
			print(DBManager.get_vacancies_with_keyword(conn, word))
		else:
			print('Программа завершена.')
			DBManager.quit(conn)
			break


if __name__ == '__main__':
	user_interaction()
