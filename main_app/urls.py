"""MyFolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https:
    //docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path
from main_app import views
from main_app.views import *

urlpatterns = [
    path('', views.introduction_page, name='introduction'),
    path('new_account', views.new_account, name='new_account'),
    path('home', BlogView.as_view(), name='home'),
    path('user_profile', GeneralDetails.as_view(), name='user_profile'),
    path('login', views.verify_user, name='verify_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('profile/<slug:name>/', views.public_profile, name='public_profile'),
    path('post/<slug:post_id>', views.public_post, name='public_post'),
    path('search/<slug:search>', views.search_result, name='search_results')
]
