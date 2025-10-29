from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from .models import Application, Category


def index(request):
    completed_applications = Application.objects.filter(status='completed').order_by('-created_at')[:4]
    in_progress_count = Application.objects.filter(status='in_progress').count()

    context = {
        'completed_applications': completed_applications,
        'in_progress_count': in_progress_count,
    }
    return render(request, 'index.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_value = form.cleaned_data['login']
            password = form.cleaned_data['password']

            user = authenticate(request, username=login_value, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/superadmin/')
                return redirect('index')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['login']
            user.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'user/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')