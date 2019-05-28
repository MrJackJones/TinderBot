# Tinder Bot

## 1. Installations

1.1. Install sowtware for ubuntu:
```bash
sudo apt-get update
sudo apt-get install nginx mysql-server python3-pip python3-dev libmysqlclient-dev ufw virtualenv
```

1.2. Create virtualenv
```bash
virtualenv venv
```

1.3. Enter in virtualenv
```bash
source venv/bin/activate 
```
1.4. Install requirements
```bash
pip install -r requirements.txt
```

1.5. Create makemigrations and run server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
1.6. Create superuser
```bash
python manage.py createsuperuser
```

1.7 Go to admin panel and enter superuser login and password
```bash
http://127.0.0.1:8000/admin/
```


## 2. Administration

### 2.1. Create profile

2.1.1. Go to profile page: http://127.0.0.1:8000/admin/main/profile/

2.1.2. Click the button "add profile"

2.1.3. Select Gender and Country (you can use manual settings click to "manual" checkbox), if the manual setting button is not selected, the profile will be automatically generated 

### 2.2. Add proxy

2.2.1. Go to profile page: http://127.0.0.1:8000/admin/main/proxylist/

2.2.2. Click the button "add proxy list"

2.2.3. Enter Country name and add TXT file with proxy and click "save" button


### 2.3. Create bot

2.3.1. Go to profile page: http://127.0.0.1:8000/admin/main/bot/

2.3.2. Click the button "add bot"

2.3.3. Select Profile from point 1 if you need to use proxy select proxy, for manual activation select "manual" add enter a phone number

2.3.4. Select "Bot is active" and click "save"

2.3.5. After save bot click "Get Auto Token" button and wait a token, or if you select "manual" send SMS to manual phone number and wait sms

### 2.4. Run bot

2.4.1. After activation bot you will see token and Bot is active is green icon

2.4.2. Run likes script use command: 
```python
python scripts/likes.py run
```

2.4.3. Run check token script use command:
```python
python scripts/check_token.py run
```

2.4.4. You can see a likes profile in: http://127.0.0.1:8000/admin/main/likesprofile/


