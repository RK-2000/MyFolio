from django.shortcuts import render, redirect
from main_app.forms import VerifyUser, NewUserForm, AddBlog
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from main_app.models import Blog
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import FormView, ListView


# Create your views here.

# Page that user will see when he visits the site for the first time.
def introduction_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'index.html')


# Page that he will see after clicking on make new account
def new_account(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect('home')


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
        return redirect('home')


# Home page for logged in users

class BlogView(LoginRequiredMixin, FormView, ListView):
    login_url = 'verify_user'
    redirect_field_name = 'home'

    model = Blog
    context_object_name = 'all_blog'
    template_name = 'home.html'
    form_class = AddBlog

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('home')


# Logging out
def logout_user(request):
    logout(request)
    return redirect('introduction')
