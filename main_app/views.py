from django.shortcuts import render, redirect
from main_app.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from main_app.models import *
from django.views.generic import FormView, ListView, View
import re
# Functions

from PIL import Image, ImageDraw, ImageFilter


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


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
                first_name = (form.cleaned_data['first_name'].lower()).capitalize()
                last_name = (form.cleaned_data['last_name'].lower()).capitalize()
                email = form.cleaned_data['email'].lower()
                username = form.cleaned_data['enrollment_no'].lower()
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

class BlogView(LoginRequiredMixin, View):
    login_url = 'verify_user'
    redirect_field_name = 'home'
    template_name = 'home.html'

    def get(self, request):
        data = Blog.objects.all()
        form = {'searchForm': SearchForm(), 'addBlog': AddBlog()}
        if data is not None:
            for d in data:
                if d.image is not None:
                    im = Image.open(d.image)
                    thumb_width = 640
                    im_thumb = expand2square(im, (0, 0, 0)).resize((thumb_width, thumb_width), Image.LANCZOS)
                    loc = 'media/' + str(d.image)
                    im_thumb.save(loc)
        return render(request, 'home.html', {'data': data, 'form': form})

    def post(self, request):
        if self.request.POST.get('form_type') == 'search':
            form = SearchForm(request.POST)
            search = (form['search'].value()).lower()
            return redirect(search_result, **{'search': search})
        else:
            form = AddBlog(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.instance.author_fn = request.user.first_name + " " + request.user.last_name
                form.save()
                return redirect('home')


# search result
def search_result(request, search):
    if request.user.is_authenticated:
        data = {}
        if re.search('(0187[a-zA-Z]{2}[0-9]{6})', search):
            d = User.objects.filter(username=search).first()
            data['by_user'] = d
        else:
            skill = None
            skill = Skill.objects.filter(skill_name=search).first()
            search = (search.lower()).capitalize()
            print(search)
            p = []
            if skill is not None:
                print(skill)
                d = UserSkills.objects.filter(skill_id=skill.skill_id).all()
                for d1 in d:
                    p.append(User.objects.filter(username=d1.user).first())
                data['by_skill'] = p
            else:
                if User.objects.filter(first_name=search).first():
                    d = User.objects.filter(first_name=search).all()
                    print(d)
                    data['by_f_name'] = d
                elif User.objects.filter(last_name=search).first():
                    d = User.objects.filter(last_name=search).all()

                    data['l_name'] = d
        count = 1
        for d in data:
            count = count + 1
        return render(request, 'search_result.html', {'data': data,'count':count})
    else:
        return redirect('verify_user')


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
        skills = UserSkills.objects.filter(user=self.request.user).all()
        stars = []
        if skills is not None:
            for skill in skills:
                star = []
                for i in range(0, int(skill.expertise)):
                    star.append('*')
                stars.append(star)
        if data:
            if data.profile_picture:
                im = Image.open(data.profile_picture)
                thumb_width = 320
                im_thumb = crop_max_square(im).resize((thumb_width, thumb_width), Image.LANCZOS)
                loc = 'media/' + str(data.profile_picture)
                im_thumb.save(loc)
        form = {}
        if data is not None:
            form['form1'] = CompleteUserForm(instance=data)
        else:
            form['form1'] = CompleteUserForm()

        form['form2'] = LinksForm()
        form['form3'] = EducationForm()
        form['form4'] = ProjectsForm()
        form['form5'] = SkillsForm()
        return render(request, 'complete_profile.html',
                      {'data': data, 'links': links, 'educations': educations, 'projects': projects, 'stars': stars,
                       'skills': skills,
                       'form': form})

    def post(self, request):
        if self.request.POST.get('form_type') == 'form1':
            data = UserCompleteProfile.objects.filter(user=self.request.user).first()
            form1 = CompleteUserForm(request.POST, request.FILES, instance=data)
            form1.instance.user = self.request.user
            if form1.is_valid():
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
        elif self.request.POST.get('form_type') == 'form5':
            form5 = SkillsForm(request.POST)
            form5.instance.user = self.request.user
            if form5.is_valid():
                form5.save()
                return redirect('user_profile')


# Show public profile

def public_profile(request, name):
    user = User.objects.filter(username=name).first()
    if request.user.is_authenticated:
        data = UserCompleteProfile.objects.filter(user=user).first()
        if data:
            if data.profile_picture:
                im = Image.open(data.profile_picture)
                thumb_width = 320
                im_thumb = crop_max_square(im).resize((thumb_width, thumb_width), Image.LANCZOS)
                loc = 'media/' + str(data.profile_picture)
                im_thumb.save(loc)
        links = Link.objects.filter(user=user).all()
        projects = Project.objects.filter(user=user).all()
        education = Education.objects.filter(user=user).all()
        skills = UserSkills.objects.filter(user=user).all()

        return render(request, 'public_user_profile.html', {
            'user': user,
            'data': data,
            'links': links,
            'projects': projects,
            'educations': education,
            'skills': skills
        })
    else:
        return redirect('verify_user')


def public_post(request, post):
    blog = Blog.objects.filter(blog_id=post).first()
    if request.user.is_authenticated:
        return render(request, 'public_post.html', {'blog': blog})
    else:
        return render(request, 'verify_user.html')


# Logging out
def logout_user(request):
    logout(request)
    return redirect('introduction')
