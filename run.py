import time
import json
from adidas import Adidas

def main():
    settings = load_data('settings.json')

    adidas = Adidas(settings)

    # it can be used in cases when we have to use new capcha token
    site_key = adidas.get_site_key()
    if not site_key:
        print('Не удалось получить site_key идентификатор капчи')
    
    # sku = 'FH7362_720'
    # sku = 'AC7841_660'
    # format like that - 55.755826 37.6173, 57.81925 28.332065
    raw_locations = input('Введите список координат:')
    sku = input('Введите SKU:')
    uniqs_stores = adidas.get_filtered_data(raw_locations, sku)

    if uniqs_stores:
        t = time.strftime('%H.%M.%S', time.localtime())
        adidas.dump_data(f'{t} {sku}.json', uniqs_stores)

        print(f'{sku} -> {len(uniqs_stores)} полностью фильтрованных магазинов')
        print(f'{t} {sku}.json -> сохранен')
        input()

def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print(f'Не удалось найти файл {filename}')

if __name__ == '__main__':
    main()