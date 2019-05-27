import os
import sys
import django
import logging
import requests

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + "/../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewChatBot.settings")
django.setup()

log_path = f"{current_path}/logs/check_token.log"

from time import sleep
from scripts.lib.daemon import Daemon
from main.models import *
from NewChatBot.constants import *

logging.basicConfig(filename=log_path, level=LOGGING_LEVEL, format=LOGGING_FORMAT)


class CheckTokenDaemon(Daemon):
    def run(self):
        while True:

            bots = Bot.objects.filter(bot_is_active=True)

            for bot in bots:
                headers = {'x-auth-token': bot.token}
                response = requests.get(f'https://api.gotinder.com/meta', headers=headers)
                if response.status_code != 200:
                    msg = f'Bot {bot.id} token in disabled'
                    logging.error(msg)
                    bot.token_is_active = False
                    bot.bot_is_active = False
                    bot.save()

                sleep(120)


if __name__ == '__main__':
    daemon = CheckTokenDaemon("{}/check_token.pid".format(current_path), stderr=log_path + '.err')

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
