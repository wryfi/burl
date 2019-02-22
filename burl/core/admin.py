from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BurlUser


admin.site.register(BurlUser, UserAdmin)
