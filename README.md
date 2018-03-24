# mst-test-case
MST test case

Для отправления запросов в примерах используется [httpie](https://httpie.org/).

##### Пример GET запроса для получения списка книг с параметрами:
  `http GET <server>/api/books?cat_id=2&price_min=2000&price_max=3000`
  
Доступные параметры (опциональны):
- `price_min` – минимальная цена (логично, не может быть больше `price_max` – отдаст `400 Bad Request`)
- `price_max` – максимальная цена (то же самое наоборот :) )
- `cat_id` – id категории книг
  
##### Пример POST запроса для создания транзакции:
  `http POST <server>/api/transactions user_id=1 books_ids:='[1, 2, 3]'`

В случае попытки передать POST без `Content-Type: application/json` будет вызван `415 Unsupported Media Type`. (Как и 400, и 404 в необходимых ситуациях.)
