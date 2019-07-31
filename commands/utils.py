import requests
import json


def _get(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        if res.status_code != 200:
            raise Exception(res.text)

        res_dict = dict()
        res_dict['content'] = json.loads(res.text)
        res_dict['error'] = False
        return res_dict

    except Exception as ex:
        print('At _get(): ')
        err_json = dict()
        err_json['content'] = str(ex)
        err_json['error'] = True
        return err_json
