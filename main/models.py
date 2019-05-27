from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.safestring import mark_safe
from NewChatBot.constants import *
from django.db.models.signals import post_save, pre_save
import requests
import json
from datetime import datetime
import pytz
import ssl
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from NewChatBot.constants import *


class ProxyList(models.Model):
    country = models.CharField(max_length=255)
    proxy_list = models.FileField()

    def __str__(self):
        return self.country


class Profile(models.Model):
    gender = models.PositiveSmallIntegerField('Gender', choices=ALL_GENDER, default=male)
    country = models.CharField('Country', choices=COUNTRY_ALL, default='random', max_length=255)
    manual = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to='images', blank=True, null=True)
    show_gender_on_profile = models.BooleanField(default=False)

    def photo_tag(self):
        return mark_safe(f'<img src="{BASE_HOST}media/{self.photo}" width="150" height="170"  />')

    photo_tag.short_description = 'Image'
    photo_tag.allow_tags = True

    def __str__(self):
        return f"{self.name} - {timezone.localtime(self.birth_date).strftime('%Y-%m-%d')} - {self.get_gender_display()}"


class Bot(models.Model):
    profile = models.ForeignKey(Profile, related_name='Profile', on_delete=models.CASCADE)
    proxy = models.ForeignKey(ProxyList, related_name='proxy', on_delete=models.CASCADE, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+79999999999'. Up to 15 digits allowed.")
    sms_regex = RegexValidator(regex=r'^\+?1?\d{6,6}$')
    manual = models.BooleanField(default=False)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    phone_country = models.PositiveSmallIntegerField('Phone Country', choices=PHONE_COUNTRY, default=7)
    sms_code = models.CharField(validators=[sms_regex], max_length=6, blank=True, null=True)
    token = models.CharField(max_length=36, blank=True, null=True)
    bot_is_active = models.BooleanField(default=False)
    token_is_active = models.BooleanField(default=False)


class LikesProfile(models.Model):
    name = models.CharField(max_length=255)
    profile_id = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)

    def photo_tag(self):
        return mark_safe(f'<img src="{self.photo}" width="150" height="170"  />')

    photo_tag.short_description = 'Image'
    photo_tag.allow_tags = True

    def __str__(self):
        return self.name


def profile_pre_save(sender, **kwargs):
    profile = kwargs.get('instance')
    if not profile.pk and not profile.manual:
        response = requests.get(f'https://api.namefake.com/{profile.country}/{profile.get_gender_display().lower()}/', verify=False)
        data = json.loads(response.text.encode('utf-8'))

        profile.name = data['name'].split(' ')[0]
        profile.email = f"{data['email_u']}@{data['email_d']}"
        profile.latitude = data['latitude']
        profile.longitude = data['longitude']
        profile.birth_date = pytz.timezone('US/Eastern').localize(datetime.strptime(data['birth_data'], "%Y-%m-%d"), is_dst=None)

        response = requests.get(f'https://randomuser.me/api/?gender={profile.get_gender_display().lower()}', verify=False)

        data = json.loads(response.text.encode('utf-8'))

        photo = data['results'][0]['picture']['large']

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(photo, context=ctx).read())
        img_temp.flush()

        profile.photo = InMemoryUploadedFile(img_temp,'ImageField', "profile_images.jpg", 'image/jpeg', sys.getsizeof(img_temp), None)



pre_save.connect(profile_pre_save, sender=Profile)