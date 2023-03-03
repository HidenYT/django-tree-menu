from django.contrib import admin
from django import forms
from .models import TreeMenuItem, TreeMenu
# Register your models here.


admin.site.register(TreeMenu)
admin.site.register(TreeMenuItem)