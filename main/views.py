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
from django.conf import settings
from os import walk
import logging

logger = logging.getLogger('views')


def _get_phone_number(profile: Profile, proxies: dict, random_county: int):
    print('Start Get Number')

    get_number_url = f'https://onlinesim.ru/api/getNum.php?apikey={SMS_SERVICE_API_KEY}&service=tinder&country={random_county}'

    try:
        response = requests.get(get_number_url, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
    except Exception as e:
        return

    print(response.text)

    data = json.loads(response.text.encode('utf-8'))

    tzid = data['tzid']

    monitoring_number_url = f'https://onlinesim.ru/api/getState.php?apikey={SMS_SERVICE_API_KEY}&tzid={tzid}&service=tinder'

    try:
        response = requests.get(monitoring_number_url, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
    except Exception as e:
        return

    print(response.text)

    data = json.loads(response.text.encode('utf-8'))

    for i in data:
        if i['tzid'] == tzid and i.get('number') and not PhoneBlackList.objects.filter(
                phone_number=i['number']).exists():
            phone_number = i['number']
            tzid = i['tzid']

            PhoneBlackList.objects.create(phone_number=phone_number)

            return phone_number, tzid

    return


def _get_otp_code(tzid: int, proxies: dict):
    print('Start Get OTP')
    try:
        response = requests.get(
            f'https://onlinesim.ru/api/getState.php?apikey={SMS_SERVICE_API_KEY}&tzid={tzid}&service=tinder',
            proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT
        )
    except Exception as e:
        return

    print(response.text)

    data = json.loads(response.text.encode('utf-8'))
    for i in data:
        if i['tzid'] == tzid:
            if i.get('msg'):
                otp_code = i['msg']
                return otp_code
    return


@csrf_exempt
def get_token(request):
    try:
        data = json.loads(request.body.decode())
        bot_id = data['bot_id']
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

    profiles = Profile.objects.filter(bot=bot)

    random_county = bot.phone_country

    for profile in profiles:
        if profile.token_is_active:
            continue

        proxies = None
        f = None
        otp_code = None
        tzid = None

        if bot.proxy:
            proxies = get_proxy(bot.proxy.proxy_list)

        phone_number = profile.phone_number

        print(f'Start profile: {profile.pk} proxy: {proxies}')

        if not phone_number:
            while not phone_number:
                phone_number, tzid = _get_phone_number(profile, proxies, random_county)

        data = {
            "phone_number": phone_number
        }

        url = f'https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru'
        try:
            response = requests.post(url, data=data, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
        except Exception as e:
            continue
        print(response.text)

        if response.status_code != 200:
            msg = f'error_send_sms for profile: {profile.pk}'
            print(msg)
            logger.error(msg)
            continue

        repeat = 0
        while not otp_code and repeat < 5:
            sleep(20)
            otp_code = _get_otp_code(tzid, proxies)
            repeat += 1

        url = f'https://api.gotinder.com/v2/auth/sms/validate?auth_type=sms&locale=ru'

        if not phone_number and not otp_code:
            msg = f'error_not_number_or_otp_code for profile: {profile.pk}'
            print(msg)
            logger.error(msg)
            continue

        data = {
            "otp_code": otp_code,
            "phone_number": phone_number,
            "is_update": False
        }
        try:
            response = requests.post(url, data=data, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
        except Exception as e:
            continue

        if response.status_code != 200:
            msg = f'error_confirmation_sms for profile: {profile.pk}'
            print(msg)
            logger.error(msg)
            continue

        response_data = json.loads(response.text)

        refresh_token = response_data['data']['refresh_token']

        url = f'https://api.gotinder.com/v2/auth/login/sms?locale=ru'

        data = json.dumps({
            "refresh_token": refresh_token,
            "phone_number": phone_number
        })

        try:
            response = requests.post(url, data=data, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
        except Exception as e:
            continue

        if response.status_code != 200:
            msg = f'error_send_refresh_token for profile: {profile.pk}'
            print(msg)
            logger.error(msg)
            continue

        api_data = json.loads(response.text)

        if api_data['data']['is_new_user']:
            url_photo = f'https://api.gotinder.com/v2/onboarding/photo?locale=ru&requested=allow_email_marketing&requested=birth_date&requested=consents&requested=email&requested=gender&requested=name&requested=photos'
            url_profile = f'https://api.gotinder.com/v2/onboarding/fields?locale=ru&requested=allow_email_marketing&requested=birth_date&requested=consents&requested=email&requested=gender&requested=name&requested=photo'
            url_complite = f'https://api.gotinder.com/v2/onboarding/complete?locale=ru&requested=allow_email_marketing&requested=birth_date&requested=consents&requested=email&requested=gender&requested=name&requested=photos'

            onboarding_token = api_data['data']['onboarding_token']
            headers = {
                'token': onboarding_token,
            }

            f = []

            for (dirpath, dirnames, filenames) in walk(profile.photo):
                f.extend(filenames)
                break

            photo = choice(f)
            files = {'photo': ('blob', open(f'{profile.photo}/{photo}', 'rb'), 'image/jpeg')}

            try:
                photo_request = requests.post(url_photo, files=files,
                                              headers=headers, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
            except Exception as e:
                continue

            print(photo_request.text)

            if photo_request.status_code != 200:
                msg = f'error_photo_request for profile: {profile.pk}'
                print(msg)
                logger.error(msg)
                continue

            f.remove(photo)

            headers = {
                'token': onboarding_token,
                'Content-Type': 'application/json'
            }

            profile_data = json.dumps({
                "fields": [
                    {
                        "name": "birth_date",
                        "data": timezone.localtime(profile.birth_date).strftime('%Y-%m-%d')
                    },
                    {
                        "name": "email",
                        "data": profile.email
                    },
                    {
                        "name": "gender",
                        "data": profile.gender
                    },
                    {
                        "name": "show_gender_on_profile",
                        "data": profile.show_gender_on_profile
                    },
                    {
                        "name": "name",
                        "data": profile.name
                     }
                ]
            })

            try:
                profile_request = requests.post(url_profile, data=profile_data,
                                                headers=headers, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
            except Exception as e:
                continue

            print(profile_request.text)

            if profile_request.status_code != 200:
                msg = f'error_profile_request for profile: {profile.pk}'
                print(msg)
                logger.error(msg)
                continue

            complite_data = {}

            try:
                complite_request = requests.post(url_complite, data=complite_data,
                                                 headers=headers, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
            except Exception as e:
                continue

            print(complite_request.text)

            if complite_request.status_code != 200:
                msg = f'error_complite_request for profile: {profile.pk}'
                print(msg)
                logger.error(msg)
                continue
        try:
            response = requests.post(url, data=data, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
        except Exception as e:
            continue

        if response.status_code != 200:
            msg = f'error_get_api_token for profile: {profile.pk}'
            print(msg)
            logger.error(msg)
            continue

        api_data = json.loads(response.text)

        try:
            auth_complite = api_data['data']['api_token']
            profile.token = auth_complite
            profile.token_is_active = True
            profile.save()
        except:
            msg = f'error_save_api_token for profile: {profile.pk}'
            print(msg)
            logger.error(msg)
            continue

        url = f'https://api.gotinder.com/v2/meta?locale=ru'

        data = json.dumps({
            "lat": profile.latitude,
            "lon": profile.longitude,
            "force_fetch_resources": True
        })

        if auth_complite:
            headers = {
                'x-auth-token': auth_complite,
                'platform': 'web'
            }

            try:
                response = requests.post(url, data=data,
                                         headers=headers, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
            except Exception as e:
                continue

            print(response.text)

            if response.status_code != 200:
                msg = f'error_seet_geo for profile: {profile.pk}'
                print(msg)
                logger.error(msg)
                continue

            if f:
                f.remove(photo)

            while f:
                photo = choice(f)
                files = {'photo': ('blob', open(f'{profile.photo}/{photo}', 'rb'), 'image/jpeg')}

                url_photo = 'https://api.gotinder.com/image?client_photo_id=%7BphotoId%7D?client_photo_id=ProfilePhoto0000000000000&locale=ru'
                try:
                    requests.post(url_photo, files=files,
                                  headers=headers, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
                except Exception as e:
                    continue
                f.remove(photo)

        print('WAIT!')
        sleep(20)

    print('Finish')

    return JsonResponse({
            'status': 'ok',
        }, status=200)
