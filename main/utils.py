import json
import re
import requests
import random
from NewChatBot.constants import *
from django.conf import settings
from bs4 import BeautifulSoup
from django.utils import timezone
from random import randint, choice


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


def get_user_data(instance, proxies=None):
    result = None

    try:
        response = requests.get(
            f'https://fauxid.com/fake-name-generator/{instance.country}?gender={instance.get_gender_display().lower()}',
            timeout=REQUESTS_TIMEOUT, proxies=proxies, verify=False)
    except Exception as e:
        print(f'Error get fake name {e}')
        return

    html = response.text

    soup = BeautifulSoup(html, features="html.parser")

    for a in soup.find_all('a', href=re.compile(".json")):
        result = a['href']
    if not result:
        return

    response = requests.get(result)
    data = json.loads(response.text)[0]
    name_full = data['name'].split(' ')

    name = name_full[1] if name_full[0] in ['Mr', 'Mrs', 'Miss', 'Ms', 'Mx', 'Sir', 'dr', 'Dr', 'Prof.'] else name_full[0]
    email = data['email']
    latitude = data['latitude']
    longitude = data['longitude']
    birth_date = timezone.datetime.now() - timezone.timedelta(days=randint(instance.age_from, instance.age_to) * 365)

    return name, email, latitude, longitude, birth_date
