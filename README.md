В данном репо реализована сервисная часть проекта по генерации рекламных объявлений. Модель размещается либо на LLMOps платформе, либо на локальной машине.

Запуск:
1. Добавить в файл конфигурации параметры подключения к база данных postgre и redis.
2. Добавить URL, ведущий на сервис с запущенной моделью
3. Выполнить в терминале docker-compose up --build