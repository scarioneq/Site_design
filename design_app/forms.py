from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Application, Category


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, label='ФИО')
    login = forms.CharField(max_length=50, label='Логин')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)
    personal_data_agreement = forms.BooleanField(label='Согласие на обработку персональных данных')

    class Meta:
        model = CustomUser
        fields = ('full_name', 'login', 'email', 'password1', 'password2', 'personal_data_agreement')

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if CustomUser.objects.filter(login=login).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return login

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email


class LoginForm(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
