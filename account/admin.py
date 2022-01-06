from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# for show in detail of every user
UserAdmin.fieldsets[2][1]['fields'] = ('is_active', 
                                        'is_staff', 
                                        'is_superuser', 
                                        'is_author',
                                        'special_user',
                                        'groups', 
                                        'user_permissions')

# for show new attribute like is_author & etc in table of users
UserAdmin.list_display += ('is_author', 'is_special_user')

# Register your models here.
admin.site.register(User, UserAdmin)