from django.contrib import admin

from project_management.models import Meeting, Task

# Register your models here.


class MeetingAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']


admin.site.register(Meeting, MeetingAdmin)

admin.site.register(Task)
