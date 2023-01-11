from django.contrib import admin
from .models import Report
# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display=('type', 'reason', 'reported_by', 'user', 'updated')
    list_filter = ('type', 'reason')
    search_fields = ('reported_by', 'user')