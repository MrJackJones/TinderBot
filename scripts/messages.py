import os
import sys
import django
import logging
import requests
import json

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + "/../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewChatBot.settings")
django.setup()

log_path = f"{current_path}/logs/messages.log"

from time import sleep
from scripts.lib.daemon import Daemon
from main.models import *
from NewChatBot.constants import *
from main.utils import get_proxy
import dialogflow

logging.basicConfig(filename=log_path, level=LOGGING_LEVEL, format=LOGGING_FORMAT)


class MessagesDaemon(Daemon):
    def detect_intent_texts(self, project_id, session_id, text, language_code):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        if text:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)
            query_input = dialogflow.types.QueryInput(text=text_input)
            response = session_client.detect_intent(
                session=session, query_input=query_input)

            if response:
                return response.query_result.fulfillment_text
            else:
                return '))'

    def run(self):
        while True:
            proxies = None
            profiles = Profile.objects.filter(bot__bot_is_active=True, token_is_active=True)
            print(profiles)

            if not profiles:
                print('No active profile')
                exit()

            for profile in profiles:
                if profile.bot.proxy:
                    proxies = get_proxy(profile.bot.proxy.proxy_list)
                print(profile)
                headers = {'x-auth-token': profile.token}

                matches = requests.get('https://api.gotinder.com/v2/matches?count=60&locale=ru',
                                       headers=headers, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)

                response_json = json.loads(matches.text.encode('utf-8'))

                userId_response = requests.get('https://api.gotinder.com/meta',
                                               headers=headers, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
                userId_json = json.loads(userId_response.text.encode('utf-8'))
                userId = str(userId_json['user']['_id'])

                likes_profile, created = LikesProfile.objects.get_or_create(likes_profile=profile, profile_id=userId)

                for data in range(len(response_json['data']['matches'])):
                    matchId = str(response_json['data']['matches'][data]['_id'])
                    user_name = str(response_json['data']['matches'][data]['person']['name'])
                    photo = str(response_json['data']['matches'][data]['person']['name'])

                    if created:
                        likes_profile.photo = photo

                    likes_profile.name = user_name
                    likes_profile.matches = True
                    likes_profile.save()

                    if len(response_json['data']['matches'][data]['messages']) == 0:
                        post_data = {"matchId": matchId, "message": "Привет!)",
                                     "userId": userId}
                        requests.post('https://api.gotinder.com/user/matches/%s?locale=ru' % matchId, data=post_data,
                                     headers=headers, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
                    else:
                        if str(response_json['data']['matches'][data]['messages'][0]['from']) != userId:
                            message = str(response_json['data']['matches'][data]['messages'][0]['message'])

                            result = self.detect_intent_texts(DIALOGFLOW_PROJECT_ID, "unique", message, 'en')

                            post_data = {"matchId": matchId, "message": result, "userId": userId}
                            requests.post('https://api.gotinder.com/user/matches/%s?locale=ru' % matchId,data=post_data,
                                          headers=headers, proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)

                            logs = likes_profile.messages
                            likes_profile.messages = logs if logs else '' + f'{timezone.now()}: {user_name} - {message}\n'
                            likes_profile.save()

                            print(f'User: {user_name} \nQuestions: {data} \n Answer: {result}')

                sleep(20)


if __name__ == '__main__':
    daemon = MessagesDaemon("{}/messages.pid".format(current_path),
                         stderr=log_path + '.err')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'run' == sys.argv[1]:
            daemon.run()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: {} start|stop|restart".format(sys.argv[0]))
        sys.exit(2)
