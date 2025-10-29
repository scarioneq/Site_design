from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm, ApplicationForm
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


@login_required
def profile(request):
    applications = Application.objects.filter(user=request.user).order_by('-created_at')

    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'user/profile.html', context)


@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('profile')
    else:
        form = ApplicationForm()

    return render(request, 'application/create.html', {'form': form})


@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)

    if not application.can_be_deleted():
        messages.error(request, 'Нельзя удалить заявку, которая уже принята в работу или выполнена')
        return redirect('profile')

    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Заявка успешно удалена')
        return redirect('profile')

    return render(request, 'application/delete_confirm.html', {'application': application})