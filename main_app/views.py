from django.shortcuts import render, redirect
from main_app.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from main_app.models import *
from django.views.generic import FormView, ListView, View


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


# complete profile
class GeneralDetails(LoginRequiredMixin, View):
    login_url = 'verify_user'
    redirect_field_name = 'general_edit'
    form_class = CompleteUserForm
    template_name = 'complete_profile.html'

    def get(self, request):

        data = UserCompleteProfile.objects.filter(user=self.request.user).first()
        links = Link.objects.filter(user=self.request.user).all()
        educations = Education.objects.filter(user=self.request.user).all()
        projects = Project.objects.filter(user=self.request.user).all()
        form = {}
        if data is not None:
            form['form1'] = CompleteUserForm(instance=data)
        else:
            form['form1'] = CompleteUserForm()

        form['form2'] = LinksForm()
        form['form3'] = EducationForm()
        form['form4'] = ProjectsForm()
        return render(request, 'complete_profile.html',
                      {'data': data, 'links': links, 'educations': educations, 'projects': projects, 'form': form})

    def post(self, request):
        if self.request.POST.get('form_type') == 'form1':
            form1 = CompleteUserForm(request.POST)
            form1.instance.user = self.request.user
            if form1.is_valid():
                user = UserCompleteProfile.objects.filter(user=self.request.user).first()
                if user is not None:
                    UserCompleteProfile.objects.filter(user=self.request.user).delete()
                    form1.save()
                else:
                    form1.save()
                return redirect('user_profile')
            else:
                pass
                return redirect('user_profile')

        elif self.request.POST.get('form_type') == 'form2':
            form2 = LinksForm(request.POST)
            form2.instance.user = self.request.user
            temp_link = form2['link'].value()
            name = ((temp_link.split('//')[1]).split('/')[0]).split('.')
            if name[0] == 'www':
                name = name[1].capitalize()
            else:
                name = name[0].capitalize()
            form2.instance.name = name
            if form2.is_valid():
                form2.save()
                return redirect('user_profile')
            else:
                pass
                return redirect('user_profile')

        elif self.request.POST.get('form_type') == 'form3':
            form3 = EducationForm(request.POST)
            print('on form 3')
            form3.instance.user = self.request.user
            if form3.is_valid():
                print('saved form3')
                form3.save()
                return redirect('user_profile')
            else:
                pass
                return redirect('user_profile')
        elif self.request.POST.get('form_type') == 'form4':
            form4 = ProjectsForm(request.POST)
            print('form4')
            form4.instance.user = self.request.user
            if form4.is_valid():
                form4.save()
                return redirect('user_profile')
            else:
                pass
                return redirect('user_profile')


# Show public profile

def public_profile(request, name):
    user = User.objects.filter(username=name).first()
    if request.user.is_authenticated:
        user_details = UserCompleteProfile.objects.filter(user=user).first()
        links = Link.objects.filter(user=user).all()
        projects = Project.objects.filter(user=user).all()
        education = Education.objects.filter(user=user).all()

        return render(request, 'public_user_profile.html', {
            'user': user,
            'user_details': user_details,
            'links': links,
            'projects': projects,
            'education': education
        })
    else:
        return redirect('verify_user')


# Logging out
def logout_user(request):
    logout(request)
    return redirect('introduction')
