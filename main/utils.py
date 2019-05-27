import os
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import requests
from main.models import *
from NewChatBot.constants import *
from django.utils import timezone
import random

current_path = os.path.dirname(os.path.realpath(__file__))


def get_proxy(proxy_list):
    try:
        with open(f'{current_path}/../media/{proxy_list}') as f:
            my_lines = list(f.read().splitlines())
            proxy = random.choice(my_lines)

            return {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}',
            }
    except:
        return
