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

log_path = f"{current_path}/logs/likes.log"

from time import sleep
from scripts.lib.daemon import Daemon
from main.models import *
from NewChatBot.constants import *
from main.utils import get_proxy

logging.basicConfig(filename=log_path, level=LOGGING_LEVEL, format=LOGGING_FORMAT)


class LikesDaemon(Daemon):
    def run(self):
        while True:
            proxies = None
            bots = Bot.objects.filter(bot_is_active=True)

            for bot in bots:
                if bot.proxy:
                    proxies = get_proxy(bot.proxy.proxy_list)

                print(proxies)
                headers = {'x-auth-token': bot.token}
                response = requests.get('https://api.gotinder.com/recs/core?locale=ru',
                                        headers=headers, proxies=proxies, verify=False)
                data = json.loads(response.text.encode('utf-8'))
                for count in range(len(data['results'])):
                    try:
                        id = data['results'][count]['_id']
                        name = data['results'][count]['name']
                        photo = data['results'][count]['photos'][0]['url']

                        if not LikesProfile.objects.filter(profile_id=id).first():
                            likes_profile = LikesProfile(name=name, profile_id=id, photo=photo)
                            likes_profile.save()

                            requests.get(f'https://api.gotinder.com/like/{id}?fast_match=1&locale=ru',
                                         headers=headers, proxies=proxies, verify=False)

                            text = f'You like: {name}, ID: {id}, Photo: {photo}'
                            print(text)

                    except Exception as e:
                        msg = f'Error like {e}'
                        logging.error(msg)
                        continue
                    sleep(20)


if __name__ == '__main__':
    daemon = LikesDaemon("{}/likes.pid".format(current_path),
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
