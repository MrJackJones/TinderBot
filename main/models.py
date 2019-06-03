from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from NewChatBot.constants import *
from django.db.models.signals import post_save
import requests
import json
from NewChatBot.constants import *
from random import randint, choice
from django.conf import settings
from main.utils import get_proxy


class ProxyList(models.Model):
    country = models.CharField(max_length=255)
    proxy_list = models.FileField()

    def __str__(self):
        return self.country


class PhoneBlackList(models.Model):
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.phone_number


def bio_path(instance, filename):
    return f'profile/bio_{randint(1, 9999999)}/{filename}'


class Bot(models.Model):
    profile_count = models.IntegerField(default=1, blank=True, null=True)
    gender = models.PositiveSmallIntegerField('Gender', choices=ALL_GENDER, default=male)
    age_from = models.IntegerField(default=18, blank=True, null=True)
    age_to = models.IntegerField(default=18, blank=True, null=True)
    country = models.CharField('Country', choices=COUNTRY_ALL, default='random', max_length=255)
    phone_country = models.PositiveSmallIntegerField('Phone Country', choices=PHONE_COUNTRY, default=7, blank=True, null=True)
    proxy = models.ForeignKey(ProxyList, related_name='proxy', on_delete=models.CASCADE, blank=True, null=True)
    biography = models.FileField(upload_to=bio_path)
    photo_folder_list = models.CharField(max_length=1000)
    unique_names = models.BooleanField(default=False)
    bot_is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pk}"


class Profile(models.Model):
    bot = models.ForeignKey(Bot, related_name='bot', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.PositiveSmallIntegerField('Gender', choices=ALL_GENDER, default=male)
    email = models.EmailField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    photo = models.CharField(max_length=1000, blank=True, null=True)
    show_gender_on_profile = models.BooleanField(default=False)
    biography = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    token = models.CharField(max_length=36, blank=True, null=True)
    token_is_active = models.BooleanField(default=False)
    likes_limit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {timezone.localtime(self.birth_date).strftime('%Y-%m-%d')} - {self.get_gender_display()}"


class LikesProfile(models.Model):
    likes_profile = models.ForeignKey(Profile, related_name='Bot', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    profile_id = models.CharField(max_length=255)
    photo = models.CharField(max_length=255, null=True, blank=True)
    matches = models.BooleanField(default=False)
    messaging = models.BooleanField(default=False)
    messages = models.TextField('Messages', null=True, blank=True)

    def photo_tag(self):
        return mark_safe(f'<img src="{self.photo}" width="150" height="170"  />')

    photo_tag.short_description = 'Image'
    photo_tag.allow_tags = True

    def __str__(self):
        return self.name if self.name else str(self.pk)


def bot_post_save(sender, instance, created, **kwargs):
    media_root = settings.MEDIA_ROOT

    if created:
        proxies = None
        biography = instance.biography
        photo_list = instance.photo_folder_list.split(',')

        with open(f'{media_root}/{biography}') as f:
            biography_list = list(f.read().splitlines())

        for create_profile in range(instance.profile_count):

            if instance.proxy:
                proxies = get_proxy(instance.proxy.proxy_list)

            unique_names = instance.unique_names
            profile: Profile = Profile(bot=instance)
            try:
                response = requests.get(
                    f'https://api.namefake.com/{instance.country}/{instance.get_gender_display().lower()}/',
                    timeout=REQUESTS_TIMEOUT, proxies=proxies, verify=False)
            except Exception as e:
                continue

            print(response.text)
            data = json.loads(response.text.encode('utf-8'))

            name = data['name'].split(' ')[0]
            email = f"{data['email_u']}@{data['email_d']}"
            latitude = data['latitude']
            longitude = data['longitude']

            birth_date = timezone.datetime.now()-timezone.timedelta(days=randint(instance.age_from, instance.age_to)*365)

            while unique_names:
                if Profile.objects.filter(name=name).exists() \
                        or name in ['Mr', 'Mrs', 'Miss', 'Ms', 'Mx', 'Sir', 'dr', 'Dr', 'Prof.']:
                    try:
                        response = requests.get(
                            f'https://api.namefake.com/{instance.country}/{instance.get_gender_display().lower()}/',
                            proxies=proxies, verify=False, timeout=REQUESTS_TIMEOUT)
                    except Exception as e:
                        continue

                    data = json.loads(response.text.encode('utf-8'))
                else:
                    name = data['name'].split(' ')[0]
                    email = f"{data['email_u']}@{data['email_d']}"
                    latitude = data['latitude']
                    longitude = data['longitude']
                    birth_date = timezone.datetime.now() - timezone.timedelta(
                        days=randint(instance.age_from, instance.age_to) * 365)
                    unique_names = False

            profile.name = name
            profile.email = email
            profile.gender = instance.gender
            profile.latitude = latitude
            profile.longitude = longitude
            profile.birth_date = birth_date

            if biography_list:
                bio = choice(biography_list)
                biography_list.remove(bio)
                profile.biography = bio

            photo = choice(photo_list)
            profile.photo = f'{media_root}/images/{photo}'

            profile.save()

            print('Done')


post_save.connect(bot_post_save, sender=Bot)
