from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Application, Category
from .validators import validate_latin, validate_cyrillic


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, label='ФИО', validators=[validate_cyrillic])
    login = forms.CharField(max_length=50, label='Логин', validators=[validate_latin])
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

class ApplicationForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберите категорию"
    )

    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'photo': 'Форматы: jpg, jpeg, png, bmp. Максимальный размер: 2MB',
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Название категории'}),
        }


class ApplicationAcceptForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Введите комментарий при принятии заявки в работу'
            }),
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if not comment:
            raise forms.ValidationError('Комментарий обязателен при принятии заявки в работу')
        return comment


class ApplicationCompleteForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['design_photo']

    def clean_design_photo(self):
        design_photo = self.cleaned_data.get('design_photo')
        if not design_photo:
            raise forms.ValidationError('Изображение дизайна обязательно при завершении заявки')
        return design_photo