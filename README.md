Для работы с библиотекой Celery Вам потребуется:

1. Запустить брокера на redis.
2. Запустить базу данных django на postgres.
3. Запустить админку.
4. Прописать команду celery -A movies worker -S django -l info из директории ./app для запуска воркера (Прослушивателя).
5. Прописать команду celery -A movies beat -l INFO из директории ./app для запуска выполнения Periodic Tasks(Отложенных задач).
6. В админ панели создать задачу (Periodic Tasks) и функцией выбрать most_popular_films, для keywords argument указать в формате json необходимые аргументы для шаблона.  


