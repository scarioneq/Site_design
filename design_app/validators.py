import re
import os
from django.core.exceptions import ValidationError

def validate_cyrillic(value):
    if not re.match(r'^[А-Яа-яёЁ\s-]+$', value):
        raise ValidationError('ФИО должно содержать только кириллические буквы, дефис и пробелы.')


def validate_latin(value):
    if not re.match(r'^[a-zA-Z-]+$', value):
        raise ValidationError('Логин должен содержать только латинские буквы и дефис.')


def validate_image_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:  # 2MB
        raise ValidationError("Максимальный размер файла 2MB")


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Неподдерживаемый формат изображения. Разрешенные форматы: jpg, jpeg, png, bmp')