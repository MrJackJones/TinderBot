import os
import requests
import random
from NewChatBot.constants import *
from django.conf import settings


def get_proxy(proxy_list):
    media_root = settings.MEDIA_ROOT

    try:
        with open(f'{media_root}/{proxy_list}') as f:
            my_lines = list(f.read().splitlines())
            proxy = random.choice(my_lines)

            proxies = {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}',
            }

            checked_proxy = False
            repeat = 0

            while not checked_proxy and repeat < 15:

                print(f'Start Check Proxy: {proxies}')

                check_proxy_url = f'https://api.exchangeratesapi.io/latest'
                try:
                    response = requests.get(check_proxy_url, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
                except Exception as e:
                    proxy = random.choice(my_lines)
                    proxies = {
                        'http': f'http://{proxy}',
                        'https': f'https://{proxy}',
                    }
                    continue

                if response.status_code != 200:
                    proxy = random.choice(my_lines)
                    proxies = {
                        'http': f'http://{proxy}',
                        'https': f'https://{proxy}',
                    }
                    continue

                checked_proxy = True
                repeat += 1

            return proxies

    except:
        return
