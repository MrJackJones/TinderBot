import os
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import requests
from main.models import *
from NewChatBot.constants import *
from django.utils import timezone
from .utils import get_proxy
from time import sleep


@csrf_exempt
def send_sms(request):
    try:
        data = json.loads(request.body.decode())
        phone_number = data['phone_number']
        bot_id = data['bot_id']
        proxies = None
    except:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_load_data',
        }, status=400)

    bot: Bot = Bot.objects.filter(id=bot_id).first()

    if not bot:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_bot_not_found',
        }, status=400)

    if bot.proxy:
        proxies = get_proxy(bot.proxy.proxy_list)

    url = f'https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru'

    data = {
        "phone_number": phone_number
    }
    response = requests.post(url, data=data, proxies=proxies)

    if response.status_code != 200:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_send_sms',
        }, status=400)

    return JsonResponse({
            'status': 'ok',
        }, status=200)


@csrf_exempt
def get_token(request):
    try:
        data = json.loads(request.body.decode())
        phone_number = None
        otp_code = None
        if data.get('phone_number'):
            phone_number = data['phone_number']
        if data.get('otp_code'):
            otp_code = data['otp_code']
        bot_id = data['bot_id']
        proxies= None
    except:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_load_data',
        }, status=400)

    bot: Bot = Bot.objects.filter(id=bot_id).first()

    print(bot)

    if not bot:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_bot_not_found',
        }, status=400)

    # Send confirmation SMS

    if bot.proxy:
        proxies = get_proxy(bot.proxy.proxy_list)

    if not bot.manual:
        response = requests.get(f'https://onlinesim.ru/api/getNum.php?apikey={SMS_SERVICE_API_KEY}&service=other&country={bot.phone_country}', proxies=proxies)
        print(response.text)

        if response.status_code != 200:
            return JsonResponse({
                'status': 'errors',
                'data': 'error_get_number',
            }, status=400)

        data = json.loads(response.text.encode('utf-8'))
        tzid = data['tzid']

        response = requests.get(f'https://onlinesim.ru/api/getState.php?apikey={SMS_SERVICE_API_KEY}&tzid={tzid}&service=other', proxies=proxies)
        print(response.text)

        data = json.loads(response.text.encode('utf-8'))

        for i in data:
            if i['tzid'] == tzid:
                phone_number = i['number']

        data = {
            "phone_number": phone_number
        }

        url = f'https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru'

        response = requests.post(url, data=data, proxies=proxies)
        print(response.text)

        if response.status_code != 200:
            return JsonResponse({
                'status': 'errors',
                'data': 'error_send_sms',
            }, status=400)

        response = requests.get(f'https://onlinesim.ru/api/getState.php?apikey={SMS_SERVICE_API_KEY}&tzid={tzid}&service=other', proxies=proxies)
        print(response.text)

        data = json.loads(response.text.encode('utf-8'))
        repeat = 0
        while not otp_code or repeat == 20:
            for i in data:
                if i['tzid'] == tzid:
                    if i.get('msg'):
                        otp_code = i['msg']
                    else:
                        sleep(10)
                        response = requests.get(
                            f'https://onlinesim.ru/api/getState.php?apikey={SMS_SERVICE_API_KEY}&tzid={tzid}&service=other',
                            proxies=proxies)
                        print(response.text)
                        data = json.loads(response.text.encode('utf-8'))
                        repeat += 1

    url = f'https://api.gotinder.com/v2/auth/sms/validate?auth_type=sms&locale=ru'

    if not phone_number and not otp_code:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_not_number_or_otp_code',
        }, status=400)

    data = {
        "otp_code": otp_code,
        "phone_number": phone_number,
        "is_update": False
    }

    response = requests.post(url, data=data, proxies=proxies)

    if response.status_code != 200:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_confirmation_sms',
        }, status=400)

    # Send refresh token

    response_data = json.loads(response.text)

    refresh_token = response_data['data']['refresh_token']

    url = f'https://api.gotinder.com/v2/auth/login/sms?locale=ru'

    data = json.dumps({
        "refresh_token": refresh_token,
        "phone_number": phone_number
    })

    response = requests.post(url, data=data, proxies=proxies)

    if response.status_code != 200:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_send_refresh_token',
        }, status=400)

    api_data = json.loads(response.text)

    if api_data['data']['is_new_user']:
        url_photo = f'https://api.gotinder.com/v2/onboarding/photo?locale=ru&requested=allow_email_marketing&requested=birth_date&requested=consents&requested=email&requested=gender&requested=name&requested=photos'
        url_profile = f'https://api.gotinder.com/v2/onboarding/fields?locale=ru&requested=allow_email_marketing&requested=birth_date&requested=consents&requested=email&requested=gender&requested=name&requested=photo'
        url_complite = f'https://api.gotinder.com/v2/onboarding/complete?locale=ru&requested=allow_email_marketing&requested=birth_date&requested=consents&requested=email&requested=gender&requested=name&requested=photos'

        onboarding_token = api_data['data']['onboarding_token']
        headers = {
            'token': onboarding_token,
        }

        current_path = os.path.dirname(os.path.realpath(__file__))
        files = {'photo': ('blob', open(f'{current_path}/../media/{bot.profile.photo}', 'rb'), 'image/jpeg')}

        photo_request = requests.post(url_photo, files=files, headers=headers, proxies=proxies)

        if photo_request.status_code != 200:
            return JsonResponse({
                'status': 'errors',
                'data': 'error_photo_request',
            }, status=400)

        headers = {
            'token': onboarding_token,
            'Content-Type': 'application/json'
        }

        profile_data = json.dumps({
            "fields": [
                {
                    "name": "birth_date",
                    "data": timezone.localtime(bot.profile.birth_date).strftime('%Y-%m-%d')
                },
                {
                    "name": "email",
                    "data": bot.profile.email
                },
                {
                    "name": "gender",
                    "data": bot.profile.gender
                },
                {
                    "name": "show_gender_on_profile",
                    "data": bot.profile.show_gender_on_profile
                },
                {
                    "name": "name",
                    "data": bot.profile.name
                 }
            ]
        })

        profile_request = requests.post(url_profile, data=profile_data, headers=headers, proxies=proxies)

        if profile_request.status_code != 200:
            return JsonResponse({
                'status': 'errors',
                'data': 'error_profile_request',
            }, status=400)

        complite_data = {}

        complite_request = requests.post(url_complite, data=complite_data, headers=headers, proxies=proxies)

        if complite_request.status_code != 200:
            return JsonResponse({
                'status': 'errors',
                'data': 'error_complite_request',
            }, status=400)

    response = requests.post(url, data=data, proxies=proxies)

    if response.status_code != 200:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_get_api_token',
        }, status=400)

    api_data = json.loads(response.text)

    try:
        auth_complite = api_data['data']['api_token']
        bot.token = auth_complite
        bot.token_is_active = True
        bot.save()
    except:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_save_api_token',
        }, status=400)

    url = f'https://api.gotinder.com/v2/meta?locale=ru'

    data = json.dumps({
        "lat": bot.profile.latitude,
        "lon": bot.profile.longitude,
        "force_fetch_resources": True
    })

    print(data)

    headers = {
        'x-auth-token': auth_complite,
        'platform': 'web'
    }

    response = requests.post(url, data=data, headers=headers, proxies=proxies)

    print(response.text)

    if response.status_code != 200:
        return JsonResponse({
            'status': 'errors',
            'data': 'error_seet_geo',
        }, status=400)

    return JsonResponse({
            'status': 'ok',
        }, status=200)
