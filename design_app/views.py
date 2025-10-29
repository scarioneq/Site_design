from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm, ApplicationForm, CategoryForm, ApplicationCompleteForm, ApplicationAcceptForm
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
                    return redirect('../admin/dashboard/')
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


def admin_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, 'Доступ запрещен')
            return redirect('index')
        return function(request, *args, **kwargs)

    return wrapper

@login_required
@admin_required
def admin_dashboard(request):
    applications = Application.objects.all().order_by('-created_at')

    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@admin_required
def change_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if not application.can_change_status():
        messages.error(request, 'Нельзя изменить статус этой заявки')
        return redirect('admin_dashboard')

    if application.can_change_to_in_progress():
        form_class = ApplicationAcceptForm
        success_status = 'in_progress'
        success_message = 'Заявка принята в работу'

    elif application.can_change_to_completed():
        form_class = ApplicationCompleteForm
        success_status = 'completed'
        success_message = 'Заявка завершена'
    else:
        messages.error(request, 'Неизвестное действие для заявки')
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=application)
        if form.is_valid():

            application.status = success_status
            application.save()
            form.save()

            messages.success(request, f'{success_message}: "{application.title}"')
            return redirect('admin_dashboard')
    else:
        form = form_class(instance=application)

    context = {
        'form': form,
        'application': application,
    }
    return render(request, 'admin/change_status.html', context)

@login_required
@admin_required
def manage_categories(request):
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно создана')
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'admin/categories.html', context)


@login_required
@admin_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Категория "{category_name}" и все связанные заявки удалены')
        return redirect('manage_categories')

    context = {
        'category': category,
    }
    return render(request, 'admin/delete_category.html', context)