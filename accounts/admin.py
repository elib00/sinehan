from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('email', 'username')
    search_fields = ('email', 'username')

admin.site.register(CustomUser, UserAdmin)