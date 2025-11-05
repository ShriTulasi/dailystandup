from django.contrib import admin
from .models import User,Project,ProjectAssignment,EmpProfile,DailyUpdates,Meeting,FCMToken,FCMNotification

from .models import DailyUpdates
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmpProfile
from django.contrib import admin
from .models import DailyUpdates



# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(EmpProfile)
# admin.site.register(DailyUpdates)
admin.site.register(Meeting)


admin.site.register(FCMToken)
admin.site.register(FCMNotification)


class EmpProfileInline(admin.StackedInline):  
    model = EmpProfile
    can_delete = False
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = [EmpProfileInline]   # show profile in user admin
    list_display = ("username", "email", "get_phone", "is_active", "is_staff")
    search_fields = ("username", "email", "empprofile__phone")

    def get_phone(self, obj):
        return obj.empprofile.phone if hasattr(obj, "empprofile") else "-"
    get_phone.short_description = "Phone"

# Re-register User with custom admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)




class ProjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('project', 'assigned_employees', 'assigned_at')  # show employees in list

    # Custom method to display employees
    def assigned_employees(self, obj):
        return ", ".join([e.username for e in obj.employee.all()])
    assigned_employees.short_description = "Employees Assigned"

admin.site.register(ProjectAssignment, ProjectAssignmentAdmin)



@admin.register(DailyUpdates)
class DailyUpdatesAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "task_date", "short_description")  # use method instead of raw field
    search_fields = ("user__username", "project__name", "task_description")
    list_filter = ("task_date", "project__name")

    def short_description(self, obj):
        if obj.task_description:
            return (obj.task_description[:50] + "...") if len(obj.task_description) > 50 else obj.task_description
        return "-"
    short_description.short_description = "Task Description"
