# Make This Order

Приложение на Django для управления заказами в кафе или ресторане.

## Функции системы:

- **Добавление заказа**:
  Пользователь вводит номер стола и список блюд с ценами, система автоматически добавляет заказ с уникальным ID, рассчитанной стоимостью и статусом “в ожидании”.

- **Удаление заказа**:
  Пользователь выбирает заказ по ID и удаляет его из системы.

- **Поиск заказа**:
  Возможность поиска заказов по ID, номеру стола или статусу.

- **Отображение всех заказов**:
  Веб-страница с таблицей всех заказов, отображающей их ID, номер стола, список блюд, общую стоимость и статус.

- **Изменение статуса заказа**:
  Пользователь выбирает заказ по ID и изменяет его статус (“в ожидании”, “готово”, “оплачено”).

- **Расчет выручки за смену**:
  Отдельная страница или модуль для расчета общего объема выручки за заказы со статусом “оплачено”.

## Инструкция

Проект можно найти по ссылке: [Make This Order](https://menyukhov.fvds.ru/login/)
1. [Логин](https://menyukhov.fvds.ru/login/)
2. [Панель управления заказами](https://menyukhov.fvds.ru/orders/)
3. [Админка](https://menyukhov.fvds.ru:2106/admin/)
4. [Документация API](http://menyukhov.fvds.ru/api/v1/swagger/). Создать ключ можно в [Админке](https://menyukhov.fvds.ru:2106/admin/).

## Запуск проекта
1. Создаейте файл `.env` по примеру `env.example`.
2. Запустите билд и запуск контейнеров.
```bash
docker compose up -d
```
3. Проведите миграции.
```bash
docker compose exec web python manage.py migrate
```
4. Скопируйте статику.
```bash
docker compose exec web cp -r /app/staticfiles/. /static/
```
5. Создайте суперпользователя, если нужно.
```bash
docker compose exec web python manage.py createsuperuser
```

## Покрытие тестами

Результаты покрытия тестами для проекта:
| File                                                  | Stmts | Miss | Cover |
|-------------------------------------------------------|-------|------|-------|
| `src/apps/dishes/admin.py`                            | 10    | 0    | 100%  |
| `src/apps/dishes/api/serializers.py`                  | 7     | 0    | 100%  |
| `src/apps/dishes/api/urls.py`                         | 6     | 0    | 100%  |
| `src/apps/dishes/api/views.py`                        | 9     | 0    | 100%  |
| `src/apps/dishes/apps.py`                             | 5     | 0    | 100%  |
| `src/apps/dishes/models.py`                           | 11    | 1    | 91%   |
| `src/apps/orders/admin.py`                            | 23    | 1    | 96%   |
| `src/apps/orders/api/serializers.py`                  | 50    | 1    | 98%   |
| `src/apps/orders/api/urls.py`                         | 6     | 0    | 100%  |
| `src/apps/orders/api/views.py`                        | 38    | 1    | 97%   |
| `src/apps/orders/apps.py`                             | 9     | 0    | 100%  |
| `src/apps/orders/data_types.py`                       | 13    | 0    | 100%  |
| `src/apps/orders/filters.py`                          | 8     | 0    | 100%  |
| `src/apps/orders/models.py`                           | 35    | 2    | 94%   |
| `src/apps/orders/services/order_creator.py`           | 19    | 0    | 100%  |
| `src/apps/orders/services/order_updater.py`           | 24    | 4    | 83%   |
| `src/apps/orders/services/total_revenue_getter.py`    | 31    | 2    | 94%   |
| `src/apps/orders/signals.py`                          | 6     | 0    | 100%  |
| `src/apps/orders/urls.py`                             | 4     | 0    | 100%  |
| `src/apps/orders/views.py`                            | 10    | 0    | 100%  |
| `src/apps/tables/admin.py`                            | 9     | 0    | 100%  |
| `src/apps/tables/api/serializers.py`                  | 7     | 0    | 100%  |
| `src/apps/tables/api/urls.py`                         | 6     | 0    | 100%  |
| `src/apps/tables/api/views.py`                        | 9     | 0    | 100%  |
| `src/apps/tables/apps.py`                             | 5     | 0    | 100%  |
| `src/apps/tables/models.py`                           | 12    | 1    | 92%   |
| `src/core/models.py`                                  | 6     | 0    | 100%  |
| `src/core/services.py`                                | 16    | 2    | 88%   |
| `src/core/settings.py`                                | 45    | 3    | 93%   |
| `src/core/urls.py`                                    | 9     | 0    | 100%  |
| **TOTAL**                                             | **448** | **18** | **96%** |
