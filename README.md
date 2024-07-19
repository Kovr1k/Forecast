# Forecast
Веб-приложение для определения погоды

Сделаны автодополнение (подсказки) при вводе города

Для запуска необходимо:
  1. Открыть папку с проектов в среде разработки (Например VSCode или PyCharm)
  2. Создать терминал и установить библиотеки следующими командами по очереди:
      - pip install django
      - pip install requests
      - pip install requests-cache retry-requests numpy pandas
      - pip install openmeteo-requests
      - pip install geopy
  3. Провести миграции командой py manage.py migrate
  4. Запустить локальный сервер командой py manage.py runserver
  5. Открыть в браузере адрес http://127.0.0.1:8000/
