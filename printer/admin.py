# 6. admin 등록 (admin.py)
from django.contrib import admin
from .models import DeviceInfo, ASRequest

admin.site.register(DeviceInfo)
@admin.register(ASRequest)
class ASRequestAdmin(admin.ModelAdmin):
    list_display = ['device', 'symptom', 'submitter', 'submitted_at', 'is_completed']
    list_filter = ['is_completed']