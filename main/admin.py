from django.contrib import admin
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'show_gender_on_profile', 'birth_date', 'photo_tag')

    class Media:
        js = (
            'js/hide_attribute_profile.js',
        )


@admin.register(ProxyList)
class ProxyListAdmin(admin.ModelAdmin):
    list_display = ('country',)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('profile', 'phone_number', 'token', 'bot_is_active', 'token_is_active', 'auth')

    readonly_fields = ('token', 'token_is_active')
    exclude = ('sms_code',)

    def auth(self, obj):
        return render_to_string('auth.html', context={
            'obj': obj,
        })

    class Media:
        js = (
            'js/auth.js',
            'js/hide_attribute.js',
        )


@admin.register(LikesProfile)
class LikesProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_tag')
    readonly_fields = ('profile_id',)


admin.site.unregister(User)
admin.site.unregister(Group)