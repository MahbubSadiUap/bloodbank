from django import forms
from django.contrib.auth.models import User
from .models import UserExtend,RequestBlood,District


class UserForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
        widgets = {
            'password': forms.PasswordInput,
        }

class UserForm2(forms.ModelForm):
    class Meta:
        model = UserExtend
        exclude = ('donor','ready_to_donate')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RequestForm(forms.ModelForm):
    class Meta:
        model = RequestBlood
        fields = "__all__"


class ChangeForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class ChangeForm2(forms.ModelForm):
    class Meta:
        model = UserExtend
        exclude = ('donor','ready_to_donate')
