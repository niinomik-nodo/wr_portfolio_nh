from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm

User = get_user_model()
# Register your models here.

class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_staff')

    fieldsets = (
        ('ユーザー情報', {'fields':('username', 'email', 'password', 'picture')}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')}),

    )

    add_fieldsets = (
        ('ユーザー情報', {
            'fields': ('username', 'email', 'password', 'confirm_password')
        }),
    )

admin.site.register(User, CustomizeUserAdmin)