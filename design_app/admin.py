from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Application

class CustomUserAdmin(UserAdmin):
    list_display = ('login', 'email', 'full_name', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('full_name', 'login', 'personal_data_agreement')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Application)