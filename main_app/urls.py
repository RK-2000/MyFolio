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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.introduction_page, name='introduction'),
    path('new_account', views.new_account, name='new_account'),
    path('home', BlogView.as_view(), name='home'),
    path('user_profile', GeneralDetails.as_view(), name='user_profile'),
    path('login', views.verify_user, name='verify_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('profile/<slug:name>/', views.public_profile, name='public_profile'),
    path('post/<slug:post_id>', views.public_post, name='public_post'),
    path('search/<str:search>', views.search_result, name='search_results'),
    path('user_profilee/<int:link_id>', views.delete_links, name='delete_links'),
    path('user_profilei/<int:skill_id>', views.delete_skills, name='delete_skills'),
    path('user_profileo/<int:edu_id>', views.delete_edu, name='delete_edu'),
    path('user_profileu/<int:pro_id>', views.delete_projects, name='delete_projects'),
    path('user_profilez/<int:blog_id>', views.delete_blogs, name='delete_blogs'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
handler404 = 'main_app.views.handler404'
handler500 = 'main_app.views.handler500'
