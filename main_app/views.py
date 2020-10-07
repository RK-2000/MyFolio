from django.shortcuts import render, redirect
from main_app.forms import VerifyUser, NewUserForm, AddBlog
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from main_app.models import Blog
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required


# Create your views here.

# Page that user will see when he visits the site for the first time.
def introduction_page(request):
    return render(request, 'index.html')


# Page that he will see after clicking on make new account
def new_account(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.all().filter(email=email).first() is None and User.objects.all().filter(
                    username=username).first() is None:
                user = User(first_name=first_name, last_name=last_name, email=email,
                            password=password,
                            username=username)
                user.save()
                print('Successful!!!')
                login(request, user)
                return redirect('home')
            else:
                print('User already found! ')
        else:
            print('Not Valid')
    else:
        form = NewUserForm()
    return render(request, 'new_account.html', {'form': form})


# login users
def verify_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = VerifyUser(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                if User.objects.all().filter(email=email).first() is not None:
                    user = User.objects.all().filter(email=email).first()
                    if user.password == password:
                        login(request, user)
                        return redirect('home')
                    else:
                        messages.error(request, 'Wrong Password! Try again')
                else:
                    messages.error(request, 'No such email found')
            else:
                messages.error(request, 'Use correct email format')
        else:
            form = VerifyUser()
        return render(request, 'verify_user.html', {'form': form})
    else:
        redirect('home')


# Home page for logged in users

def home(request):
    if request.user.is_authenticated:
        all_blog = Blog.objects.all().reverse()
        count = Blog.objects.all().count()
        return render(request, 'home.html', {'all_blog': all_blog, 'size': count})
    else:
        print('user not authenticated')
        return redirect('introduction')


def add_blog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                form = AddBlog(request.POST, request.FILES)
                form.user = request.user
                if form.is_valid():
                    form.instance.name = request.user.first_name + ' ' + request.user.last_name
                    form.save()
                    form = AddBlog()
                    print('successful')
                    return redirect('home')
                else:
                    print(form.errors, len(form.errors))
            except (IOError, ValueError, MultiValueDictKeyError):
                print('form not correct')
                return redirect('add_blog')
        else:
            form = AddBlog()
        return render(request, 'add_blog.html', {'form': form, 'user': request.user})
    else:
        return redirect('introduction')


# Logging out
def logout_user(request):
    logout(request)
    return redirect('introduction')
