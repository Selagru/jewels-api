Установка и запуск: docker-compose up


superuser: login - 'admin' password - 'q1w2e3r4'


Выдача обработанных данных: (доступные методы: GET)
	http://127.0.0.1:8000/top_5_customers/


Загрузка файла для обработки: (доступные методы: POST)
	http://127.0.0.1:8000/upload/

	Content-Type: multipart/form-data
	форма: deals - "файл.csv"

	рекомендуемый способ проверки - запрос через Insomnia / Postman.