from django.contrib import admin
from .models import Product,User,Album
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','item','price','user',"created_at"]


class UserAdmin(UserAdmin):
    
    list_display = ('id','username','email','is_active','is_staff')
    list_filter = ('id','email','username')
    
    fieldsets = [
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Information", {"fields": ("profile","title","first_name", "last_name","contact","gender","date_of_birth","state","address")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser",'last_login')}),
    ]

    add_fieldsets = [
        (None, {
        "classes": ("wide",),
        "fields": ("email", "username", "password1","password2"),
    }),
    ]


    search_fields = ('email','username')
    ordering = ('username','id')
    filter_horizontal = ()

admin.site.register(User,UserAdmin)

admin.site.register(Album)


