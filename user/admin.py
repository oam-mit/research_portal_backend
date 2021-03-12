from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User,Department,Student,Faculty,Project,Application


# Register your models here.

class StudentAdmin(admin.StackedInline):
    model=Student

    verbose_name=verbose_name_plural='Student Related Details'

class FacultyAdmin(admin.StackedInline):
    model=Faculty
    verbose_name=verbose_name_plural='Faculty Related Details'
    

class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (('Login Information'), {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name','department')}),
        (('Type of User'),{'fields':('is_student','is_faculty')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    ]

    add_fieldsets = [
        ('Enter this basic information', {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name', 'password1', 'password2'),
        }),
    ]
    list_display = ( 'email','first_name', 'last_name','is_student')
    search_fields=['email','first_name','last_name']
    ordering=['is_student','email']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            self.inlines=[FacultyAdmin,StudentAdmin]
            return self.add_fieldsets
        if obj.is_faculty:
            self.inlines=[FacultyAdmin]
        else:
            self.inlines=[StudentAdmin]
        return super().get_fieldsets(request, obj)
    
class DepartmentAdmin(admin.ModelAdmin):
    readonly_fields=['slug']

    class Meta:
        model=Department

class ProjectAdmin(admin.ModelAdmin):
    list_display=['faculty','title','description','department']
    fieldsets = [
        (('Basic Information'), {'fields': ('faculty', 'title','description')}),
        (('Tags (Separate tags with comma)'), {'fields': ('tags',)}),
        (('Control Information'),{'fields':('is_department_specific','max_students','start_date','end_date','is_active')}),
    ]

    list_filter=['faculty__user__department__name']

    def faculty(self,obj):
        return obj.faculty
    
    def department(self,obj):
        return obj.faculty.user.department.name

    class Meta:
        model=Project

class ApplicationAdmin(admin.ModelAdmin):
    list_display=['project','student','time_of_submission']
    readonly_fields=['time_of_submission']

    def project(self,obj):
        return obj.faculty
    
    def student(self,obj):
        return obj.student

    class Meta:
        model=Application

admin.site.register(User,CustomUserAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Application,ApplicationAdmin)