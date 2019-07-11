from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.utils.html import format_html, format_html_join
from django.forms import ModelForm, Select, CharField
import os
import sys


class FolderListDropDown(Select):
    def __init__(self, attrs=None):
        current_path = os.path.dirname(os.path.realpath(__file__))
        target_folder = f'{current_path}/../media/images/'
        dir_contents = os.listdir(target_folder)
        directories = []

        for item in dir_contents:
            if os.path.isdir(''.join((target_folder,item,))):
              directories.append((item, item),)

        folder_list = tuple(directories)
        super(FolderListDropDown, self).__init__(attrs=attrs, choices=folder_list)


class photoForm(ModelForm):
    photo_folder_list = CharField(widget=FolderListDropDown())


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('country', 'gender', 'ages', 'proxy', 'bot_active', 'auth')

    form = photoForm

    def ages(self, obj):
        return format_html(f'From {obj.age_from} to {obj.age_to}')

    ages.short_description = 'Age'

    def bot_active(self, obj):
        active_bot_count = Profile.objects.filter(bot=obj, token_is_active=True).count()
        bot_count = Profile.objects.filter(bot=obj).count()
        return format_html(f'{active_bot_count}/{bot_count}')

    bot_active.short_description = 'Active Profile'

    def auth(self, obj):
        return render_to_string('auth.html', context={
            'obj': obj,
        })

    class Media:
        js = (
            'js/auth.js',
        )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'bot', 'gender', 'phone_number', 'likes_limit', 'token', 'token_is_active', 'photo', 'biography', 'birth_date')

    readonly_fields = ('token', 'token_is_active')


@admin.register(ProxyList)
class ProxyListAdmin(admin.ModelAdmin):
    list_display = ('country',)


@admin.register(PhoneBlackList)
class PhoneBlackListAdmin(admin.ModelAdmin):
    list_display = ('phone_number',)


@admin.register(LikesProfile)
class LikesProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'likes_profile', 'photo_tag', 'matches', 'messaging')
    list_filter = ['likes_profile', 'matches', 'messaging']
    readonly_fields = ('profile_id',)


admin.site.unregister(User)
admin.site.unregister(Group)