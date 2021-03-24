
import requests
import json
import time
from bs4 import BeautifulSoup
from rucapcha import RuCapcha
import lxml
import re

class Adidas():
    def __init__(self, settings) -> None:
        self.s = requests.Session()
        self.rucapcha = settings['rucapcha_api_key']
        self.token = settings['prev_token']
        self.sitekey = None

    def get_site_key(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        self.s.headers.update(headers)
        r = self.s.get('https://www.adidas.ru/')
        
        soup = BeautifulSoup(r.text, 'lxml')

        # I HATE THIS SOLUTION!!!!
        for js in soup.select('script'):
            if 'recaptchaV3SiteKey' in str(js):
                key = re.findall('"recaptchaV3SiteKey":"\w+"', str(js).replace('\\',''))[0].split(':')[1][1:-1]
                self.sitekey = key

                return key

        return None

    def get_location_stores(self, lat, lon, sku):
        """
        Return inventory check results for lat lon and sku data in json
        """
        max_attempts = 5
        attempts = 0
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'referer': 'https://www.adidas.ru/',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }

        while attempts < max_attempts:
            params = {
                'isCnCRestricted': 'false',
                'lat': lat,
                'lng': lon,
                'recaptcha': self.token,
                'sku': sku
            }
            r = self.s.get('https://www.adidas.ru/api/inventory-check', params=params, headers=headers)
            r.encoding = 'utf-8'

            if r.status_code == 200:
                return json.loads(r.text)
            else:
                # adidas using recapcha based on reputation level of visitor
                # sometimes because of bad reputation level of worker from rucapcha
                # you should solve capcha one more time
                rucapcha = RuCapcha(self.rucapcha)
                captcha_id = rucapcha.send_recaptcha(self.sitekey, 'https://www.adidas.ru')
                self.token = rucapcha.get_captcha_answer(captcha_id)
                attempts += 1

                if not self.token:
                    continue

                self.dump_data('settings.json', {'rucapcha_api_key': self.rucapcha, 'prev_token': self.token})
        
        print('Превышено максимальное количество попыток получения ключа')
        return None

    def get_filtered_data(self, raw_locations, sku):
        '''
        Return only unics stores data with status availability=now for locations 
        '''
        locations = raw_locations.split(',')
    
        all_items = []
        for loc in locations:
            lat, lon = loc.strip().split()
            r = self.get_location_stores(lat, lon, sku)

            if not r:
                return []

            for store in r['filteredStores']:
                if store['availability'] == 'now':
                    all_items.append(store)
            
            print(f'{lat} | {lon} | {sku} -> {len(r.get("filteredStores"))} не фильтрованных по доступности магазинов')
            # for safety reasons
            time.sleep(3)

        uniqs = list({el['id']:el for el in all_items}.values())
        
        return uniqs

    @staticmethod
    def dump_data(filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)