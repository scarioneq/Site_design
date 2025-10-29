import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_cyrillic, validate_latin, validate_image_size, validate_image_extension


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
    photo = models.ImageField(
        upload_to='application_photos/',
        validators=[validate_image_size, validate_image_extension]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    design_photo = models.ImageField(
        upload_to='design_photos/',
        null=True,
        blank=True,
        validators=[validate_image_size, validate_image_extension]
    )
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def can_be_deleted(self):
        return self.status == 'new'