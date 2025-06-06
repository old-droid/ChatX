"""
URL configuration for ChatX project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from chat_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')), # For login/logout
    path('', views.home, name='home'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('get_messages/<int:recipient_id>/', views.get_messages, name='get_messages_with_recipient'),
]
