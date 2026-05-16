"""
URL configuration for first_project project.

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
from django.urls import path
from first_app.views import index_page
from first_app.views import time_page
from first_app.views import calc_page
from first_app.views import multiply
from first_app.views import expression
from first_app.views import history
from first_app.views import login_page
from first_app.views import logout_page
from first_app.views import str2words_page
from first_app.views import str_history_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('time/', time_page),
    path('calc/', calc_page),
    path('multiply/', multiply),
    path('expression/', expression),
    path('history/', history),
    path('login/', login_page),
    path('logout/', logout_page),
    path('str2words/', str2words_page),
    path('str_history/', str_history_view),
]
