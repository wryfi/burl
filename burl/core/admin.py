from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BurlUser


admin.site.register(BurlUser, UserAdmin)
admin.site.site_header = "burl admin"
admin.site.site_title = "burl admin"
admin.site.index_title = "home"
