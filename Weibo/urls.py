"""Weibo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^uploadfile/', views.upload_file),
    url(r'^create_wb/', views.create_wb),
    url(r'^get_new_wb_count/', views.get_new_wb_count),
    url(r'^get_new_wb/', views.get_new_wb),
    url(r'^favor/', views.favor),
    url(r'^home/$', views.home),
    url(r'^search/$', views.search),
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
]
