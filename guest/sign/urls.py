"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from sign import views_if

urlpatterns = [
    url(r'^add_event/', views_if.add_event, name='add_event'),
    url(r'^add_guest/', views_if.add_guest, name='add_guest'),
    url(r'^get_event_list/', views_if.get_event_list, name='get_event_list'),
    url(r'^get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
    url(r'^user_sign/', views_if.user_sign, name='user_sign'),
]
