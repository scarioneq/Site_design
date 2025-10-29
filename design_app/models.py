from django.contrib.auth.models import AbstractUser
from django.db import models
import re
from django.core.exceptions import ValidationError


def validate_cyrillic(value):
    if not re.match(r'^[А-Яа-яёЁ\s-]+$', value):
        raise ValidationError('ФИО должно содержать только кириллические буквы, дефис и пробелы.')


def validate_latin(value):
    if not re.match(r'^[a-zA-Z-]+$', value):
        raise ValidationError('Логин должен содержать только латинские буквы и дефис.')


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, validators=[validate_cyrillic])
    login = models.CharField(max_length=50, unique=True, validators=[validate_latin])
    email = models.EmailField(unique=True)
    personal_data_agreement = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='application_photos/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    design_photo = models.ImageField(upload_to='design_photos/', null=True, blank=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.title