from django.contrib import admin
from django.contrib.auth.models import User
from app.models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Sub_category)