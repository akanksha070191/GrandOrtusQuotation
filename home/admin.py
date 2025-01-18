from django.contrib import admin
from home.models import LogInUser


# Register your models here.
class homeAdmin(admin.ModelAdmin):
    list_display=('firstName', 'email', 'phoneNumber', 'password')

admin.site.register(LogInUser, homeAdmin)