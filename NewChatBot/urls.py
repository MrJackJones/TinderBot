"""NewChatBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from main.views import *


def get_admin_urls(urls):
    def get_urls():
        return [
                   path('main/bot/send/sms/', admin.site.admin_view(send_sms), name='send_sms'),
                   path('main/bot/get/token/', admin.site.admin_view(get_token), name='send_sms'),
               ] + urls

    return get_urls


admin.site.get_urls = get_admin_urls(admin.site.get_urls())

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)