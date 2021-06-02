from django.contrib import admin
from .models import JudgeProfile, JudgesPoll


admin.site.register(JudgesPoll)
admin.site.register(JudgeProfile)
