from django.shortcuts import render, redirect
from main_app.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from main_app.models import *
from django.views.generic import View
import re
from PIL import Image


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
                    messages.success(request, "Account created")
                    request.session.set_expiry(3600)
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "User already created for this email and enrollment id!")

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
                        request.session.set_expiry(3600)
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
        u = UserCompleteProfile.objects.filter(user=request.user).first()
        me = ''
        if u is None:
            me = 'Please Complete your profile'
        form = {'searchForm': SearchForm(), 'addBlog': AddBlog()}
        if data is not None:
            for d in data:
                if d.image is not None:
                    im = Image.open(d.image)
                    thumb_width = 640
                    im_thumb = expand2square(im, (0, 0, 0)).resize((thumb_width, thumb_width), Image.LANCZOS)
                    loc = 'media/' + str(d.image)
                    im_thumb.save(loc)
        return render(request, 'home.html', {'data': data, 'form': form, 'me': me, 'u': u})

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
            else:
                messages.error(request, "Your can only attach one image in a post. Try again!")
                return redirect('home')


# search result
def search_result(request, search):
    if request.user.is_authenticated:
        data = {}
        data['form'] = SearchForm()
        count = 0
        profile_pictures = []
        x = UserCompleteProfile.objects.filter(user=request.user).first()
        if re.search('(0187[a-zA-Z]{2}[0-9]{6})', search):
            d = User.objects.filter(username=search).all()
            if d.exists():
                data['by_user'] = d
                count = 1
            else:
                data['by_user'] = None
        else:
            skill = None
            skill = Skill.objects.filter(skill_name=search).first()
            search = (search.lower()).capitalize()

            p = []
            if skill is not None:

                d = UserSkills.objects.filter(skill_id=skill.skill_id).all()
                for d1 in d:
                    p.append(User.objects.filter(username=d1.user).first())
                    count = count + 1

                data['by_skill'] = p

            else:
                if User.objects.filter(first_name=search).first():
                    d = User.objects.filter(first_name=search).all()
                    for d1 in d:
                        count = count + 1
                    data['by_f_name'] = d
                elif User.objects.filter(last_name=search).first():
                    d = User.objects.filter(last_name=search).all()
                    for d1 in d:
                        count = count + 1
                    data['l_name'] = d
        if request.POST.get('form_type') == 'search':
            form = SearchForm(request.POST)
            search = (form['search'].value()).lower()
            return redirect(search_result, **{'search': search})

        return render(request, 'search_result.html', {'data': data, 'count': count, "images": profile_pictures, 'x': x})
    else:
        return redirect('verify_user')


# complete profile
class GeneralDetails(LoginRequiredMixin, View):
    login_url = 'verify_user'
    redirect_field_name = 'general_edit'
    template_name = 'complete_profile.html'

    def get(self, request):
        data = UserCompleteProfile.objects.filter(user=self.request.user).first()
        links = Link.objects.filter(user=self.request.user).all()
        educations = Education.objects.filter(user=self.request.user).all()
        projects = Project.objects.filter(user=self.request.user).all()
        skills = UserSkills.objects.filter(user=self.request.user).all()
        blogs = Blog.objects.filter(author=self.request.user).all()
        stars = []
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'enrollment_no': request.user.username,
        }
        about = {

        }
        if skills is not None:
            for skill in skills:
                star = []
                for i in range(0, int(skill.expertise)):
                    star.append('*')
                stars.append(star)
        if data:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'enrollment_no': request.user.username,
                'dob': data.dob,
                'phone': data.phone_no,
                'image': data.profile_picture
            }
            about = {
                'about': data.about
            }
            if data.profile_picture:
                im = Image.open(data.profile_picture)
                thumb_width = 320
                im_thumb = crop_max_square(im).resize((thumb_width, thumb_width), Image.LANCZOS)
                loc = 'media/' + str(data.profile_picture)
                im_thumb.save(loc)

        form = {}
        form['form1'] = UpdateAbout(initial=about)
        form['form2'] = LinksForm()
        form['form3'] = EducationForm()
        form['form4'] = ProjectsForm()
        form['form5'] = SkillsForm()
        form['form6'] = UpdateUser(initial=initial_data)
        form['form7'] = SearchForm()
        return render(request, 'complete_profile.html',
                      {'data': data, 'links': links, 'educations': educations, 'projects': projects, 'stars': stars,
                       'skills': skills, 'blogs': blogs,
                       'form': form})

    def post(self, request):
        if self.request.POST.get('form_type') == 'form1':
            data = UserCompleteProfile.objects.filter(user=self.request.user).first()
            form1 = UpdateAbout(request.POST)
            if form1.is_valid():
                about = form1.cleaned_data['about']
                if data is None:
                    about = UserCompleteProfile.objects.create(user=request.user, about=about)
                else:
                    data.about = about
                    data.save()
                return redirect('user_profile')
            else:
                messages.error(request, "Invalid entry in Edit about. Try again")
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
                messages.error(request, "Invalid entry in links edit form. Try again")
                return redirect('user_profile')

        elif self.request.POST.get('form_type') == 'form3':
            form3 = EducationForm(request.POST)
            form3.instance.user = self.request.user
            if form3.is_valid():
                form3.save()
                return redirect('user_profile')
            else:
                messages.error(request, "Invalid entry in add educational information. Try again")
                return redirect('user_profile')
        elif self.request.POST.get('form_type') == 'form4':
            form4 = ProjectsForm(request.POST)
            form4.instance.user = self.request.user
            if form4.is_valid():
                form4.save()
                return redirect('user_profile')
            else:
                messages.error(request, "Invalid entry in add a project. Try again")
                return redirect('user_profile')
        elif self.request.POST.get('form_type') == 'form5':
            form5 = SkillsForm(request.POST)
            form5.instance.user = self.request.user
            if form5.is_valid():
                form5.save()
                return redirect('user_profile')
            else:
                messages.error(request, "Invalid entry in add new skill form. Try again")
                return redirect('user_profile')

        elif self.request.POST.get('form_type') == 'search':
            form = SearchForm(request.POST)
            search = (form['search'].value()).lower()
            return redirect(search_result, **{'search': search})
        
        elif self.request.POST.get('form_type') == 'form6':
            form6 = UpdateUser(request.POST, request.FILES)
            if form6.is_valid():
                first_name = (form6.cleaned_data['first_name'].lower()).capitalize()
                last_name = (form6.cleaned_data['last_name'].lower()).capitalize()
                username = form6.cleaned_data['enrollment_no'].lower()
                dob = form6.cleaned_data['dob']
                image = form6.cleaned_data['image']
                phone = form6.cleaned_data['phone']
                details = UserCompleteProfile.objects.filter(user=request.user).first()
                if details is None:
                    details = UserCompleteProfile.objects.create(user=request.user, dob=dob, profile_picture=image,
                                                                 phone_no=phone)
                    details.save()
                else:
                    details.dob = dob
                    if image:
                        details.profile_picture = image
                    details.phone_no = phone
                    details.save()
                if username != request.user.username:
                    if User.objects.filter(username=username).first() is None and username != request.user.username:
                        User.objects.filter(username=self.request.user).update(first_name=first_name,
                                                                               last_name=last_name,
                                                                               username=username)
                    else:
                        messages.error(request, "Username already taken")
                return redirect('user_profile')
            else:
                print(form6.errors)
                messages.error(request, "Invalid entry in basic information. Try again")
                return redirect('user_profile')


# Delete Public Profile
def delete_links(request, link_id):
    if request.user.is_authenticated:
        link = Link.objects.filter(link_id=link_id).first()
        link.delete()
        return redirect('user_profile')
    else:
        return redirect('verify_user')


def delete_skills(request, skill_id):
    if request.user.is_authenticated:
        skill = UserSkills.objects.filter(skill_user_id=skill_id).first()
        skill.delete()
        return redirect('user_profile')
    else:
        return redirect('verify_user')


def delete_edu(request, edu_id):
    if request.user.is_authenticated:

        edu = Education.objects.filter(edu_id=edu_id).first()
        edu.delete()
        return redirect('user_profile')
    else:
        return redirect('verify_user')


def delete_projects(request, pro_id):
    if request.user.is_authenticated:
        project = Project.objects.filter(project_id=pro_id)
        project.delete()
        return redirect('user_profile')
    else:
        return redirect('verify_user')


def delete_blogs(request, blog_id):
    if request.user.is_authenticated:
        blog = Blog.objects.filter(blog_id=blog_id).first()
        blog.delete()
        return redirect('user_profile')
    else:
        return redirect('verify_user')


# Show public profile

def public_profile(request, name):
    if request.user.is_authenticated:
        user = User.objects.filter(username=name).first()
        data = UserCompleteProfile.objects.filter(user=user).first()
        x = UserCompleteProfile.objects.filter(user=request.user).first()
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
            'skills': skills,
            'x': x
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


def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def handler500(exception, template_name="500.html"):
    response = render(template_name)
    response.status_code = 500
    return response
