from django.contrib import admin
from .models import CustomUser, TempAccessCodes


admin.site.register(CustomUser)
admin.site.register(TempAccessCodes)
