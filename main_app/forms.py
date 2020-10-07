from django import forms
from django.forms import ModelForm
from main_app.models import Blog

my_error_message = {
    'invalid': ' Password should have 7 letters,a digit and a symbol',
    'required': 'This field is required'
}


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

    username = forms.CharField(max_length=15, required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'id': 'username-field',
                                          'placeholder': 'eg : iamelon',
                                          'type': 'text'}))

    password = forms.RegexField(required=True, regex='^(?=.*\d)(?=.*[a-z,A-Z])(?=.*[a-zA-Z]).{7,}$',
                                error_messages=my_error_message,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'id': 'password-field',
                                           'type': 'password'}))


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
            'description', 'image', 'name'
        ]

        def form_valid(self, form):
            form.instance.user = self.request.user

            return super(AddBlog, self).form_valid(form)
