## О скрипте

В русской версии адидаса около многих товаров есть кнопка "проверить наличие в магазине", нажав которую можно увидеть где есть товар в наличии и доступен прямо сейчас. 
Однако, есть товары, у которых такой кнопки нет, они продаются только в оффлайн магазинах. Но используя api данные по наличию таких товаров можно без проблем получить. 
Для этой цели и служит этот скрипт.

### Использование
Требуется в файле настроек указать API ключ от Rucapcha, потому что для получения данных о наличии товара необходимо решать капчу. Там используется капча, основанная на уровне доверия к посетителю,
поэтому токен капчи сохраняется в файле настроек (одним токеном можно пользоваться 1+ раза). Поскольку капчу решаются воркеры с рукапчи, у них низкий рейтинг, иногда капча будет решаться несколько раз кряду. 

Запускается скрипт через файл run.py, на вход ему подаются: список из ширины и долготы проверяемых мест через запятую и sku код товара.

#### Пример
Подаем на вход:

  * 2 места (Санкт-Петербург, Тверь): 59.895137 30.311052, 56.851976 35.916911
  * SKU: [AC7841_660](https://www.adidas.ru/botinki-dlia-khaikinga-terrex-frozetrack-winter/AC7841.html)

На выходе создается файл с содержимым:
```
[
    {
        "availability": "now",
        "city": "Санкт-Петербург",
        "coordinates": {
            "lat": 60.0031265,
            "lng": 30.3886197
        },
        "distance": {
            "unit": "km",
            "value": 12.7790887564767
        },
        "id": "RU444458",
        "isCnCStore": 0,
        "maxDeliveryDays": 0,
        "name": "adidas & Reebok Outlet, ТЦ Академический",
        "openingHours": [
            {
                "day": "monday",
                "from": "10:00",
                "to": "22:00"
            },
            {
                "day": "tuesday",
                "from": "10:00",
                "to": "22:00"
            },
            {
                "day": "wednesday",
                "from": "10:00",
                "to": "22:00"
            },
            {
                "day": "thursday",
                "from": "10:00",
                "to": "22:00"
            },
            {
                "day": "friday",
                "from": "10:00",
                "to": "22:00"
            },
            {
                "day": "saturday",
                "from": "10:00",
                "to": "22:00"
            },
            {
                "day": "sunday",
                "from": "10:00",
                "to": "22:00"
            }
        ],
        "phoneNumber": "+7(812)322-96-95",
        "street": "Гражданский пр-т 41, лит.А"
    }
]
```
