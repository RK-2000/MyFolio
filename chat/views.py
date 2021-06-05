from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main_app.views import login


# Create your views here.
def room(request, room_name):
    if request.user.is_authenticated:
        return render(request, '2.html', {'room_name': room_name, 'username': request.user})
    else:
        print('log in please')
