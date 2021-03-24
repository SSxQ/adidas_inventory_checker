import requests
import json
import time

class RuCapcha:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_recaptcha(self, sitekey, url, invisble=0, _json=1):
        # {"status":1,"request":"2122988149"}

        r = requests.post('https://rucaptcha.com/in.php',
            data={
                'key': self.api_key,
                'method':'userrecaptcha',
                'googlekey':sitekey,
                'pageurl':url,
                'invisble': invisble,
                'json': _json
        })
        resp = json.loads(r.text)

        if not resp['status']:
            raise Exception
        else:
            return resp['request']

    def get_captcha_answer(self, captcha_id, _json=1):
        time.sleep(20)

        while True:
            r = requests.get('https://rucaptcha.com/res.php', params = {
                    'key': self.api_key,
                    'action':'get',
                    'id':int(captcha_id),
                    'json': _json
            })
            
            resp = json.loads(r.text)
            
            if resp['status']:
                return resp['request']
            else:
                if resp['request'] == 'CAPCHA_NOT_READY':
                    print(resp)
                    time.sleep(6)
                else:
                    # sometimes capthca can be unsolvable (beceause of bad reputation of rucapcha worker)
                    print(resp)
                    return False