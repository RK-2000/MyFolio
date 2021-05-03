from django import forms
from django.forms import ModelForm
from main_app.models import *

my_error_message = {
    'invalid': 'Your password should have atleast 7 characters including a digit and a symbol',
    'required': 'This field is required'
}
CHOICES = ['1', '2', '3', '4', '5']


class NewUserForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'id': 'first-name-field',
                                            'placeholder': 'eg : Elon', 'type': 'text'}))
    last_name = forms.CharField(max_length=40, required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'id': 'last-name-field', 'placeholder': 'eg : Musk',
                                           'type': 'text'}))

    email = forms.RegexField(regex='^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', required=True,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'id': 'exampleInputEmail1',
                                        'placeholder': 'eg : abc@gmail.com',
                                        'type': 'email'}))

    enrollment_no = forms.RegexField(regex='(0187[a-zA-Z]{2}[0-9]{6})', required=True,
                                     widget=forms.TextInput(
                                         attrs={'class': 'form-control', 'id': 'username-field',
                                                'placeholder': 'eg : 0187cs181114',
                                                'type': 'text'}))

    password = forms.RegexField(required=True, regex='^(?=.*\d)(?=.*[a-z,A-Z])(?=.*[a-zA-Z]).{7,}$',
                                error_messages=my_error_message,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'id': 'password-field',
                                           'type': 'password'}))


class UpdateUser(forms.Form):
    first_name = forms.CharField(max_length=40, required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'id': 'first-name-field',
                                            'placeholder': 'eg : Elon', 'type': 'text'}))
    last_name = forms.CharField(max_length=40, required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'id': 'last-name-field', 'placeholder': 'eg : Musk',
                                           'type': 'text'}))
    enrollment_no = forms.RegexField(regex='(0187[a-zA-Z]{2}[0-9]{6})', required=True,
                                     widget=forms.TextInput(
                                         attrs={'class': 'form-control', 'id': 'username-field',
                                                'placeholder': 'eg : 0187cs181114',
                                                'type': 'text','pattern':'(0187[a-zA-Z]{2}[0-9]{6})'}))
    dob = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}))
    image = forms.ImageField(required=False)


class UpdateAbout(forms.Form):
    about = forms.CharField(widget=forms.Textarea())


class VerifyUser(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'exampleInputEmail1', 'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'exampleInputPassword1', 'placeholder': 'Enter Password',
               'type': 'password'}))


class AddBlog(ModelForm):
    class Meta:
        model = Blog
        fields = [
            'image', 'description'
        ]
        widgets = {

        }


class LinksForm(ModelForm):
    class Meta:
        model = Link
        fields = [
            'link'
        ]


class ProjectsForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name', 'project_desc', 'project_link'
        ]

        widgets = {

        }


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            'school_name', 'degree', 'start_year', 'end_year', 'grade'
        ]

        widgets = {
            'start_year': forms.TextInput(attrs={'type': 'date'}),
            'end_year': forms.TextInput(attrs={'type': 'date'})
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=15, required=True,
                             widget=forms.TextInput(attrs={'id': 'search_bar_input', 'placeholder': 'Search'}))


class SkillsForm(ModelForm):
    class Meta:
        model = UserSkills
        fields = [
            'skill', 'expertise'
        ]
