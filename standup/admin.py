from django.contrib import admin
from .models import User,Project,ProjectAssignment,EmpProfile,DailyUpdates,Meeting


# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(EmpProfile)
# admin.site.register(DailyUpdates)
admin.site.register(Meeting)




class ProjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('project', 'assigned_employees', 'assigned_at')  # show employees in list

    # Custom method to display employees
    def assigned_employees(self, obj):
        return ", ".join([e.username for e in obj.employee.all()])
    assigned_employees.short_description = "Employees Assigned"

admin.site.register(ProjectAssignment, ProjectAssignmentAdmin)



# admin.py
from django.contrib import admin
from .models import DailyUpdates

# @admin.register(DailyUpdates)
# class DailyUpdatesAdmin(admin.ModelAdmin):
#     list_display = ("user", "project", "task_date", "short_description")
#     search_fields = ("user__username", "project", "task_description")
#     list_filter = ("task_date", "project")

#     def short_description(self, obj):
#         # show only first 50 chars in list view
#         return (obj.task_description[:50] + "...") if len(obj.task_description) > 50 else obj.task_description
#     short_description.short_description = "Task Description"



# from django.contrib import admin
# from .models import DailyUpdates

# @admin.register(DailyUpdates)
# class DailyUpdatesAdmin(admin.ModelAdmin):
#     # display actual task_description in admin
#     list_display = ("user", "project", "task_date", "task_description")
#     search_fields = ("user__username", "project__name", "task_description")
#     list_filter = ("task_date", "project__name")

#     def short_description(self, obj):
#         # show first 50 chars with ellipsis
#         if obj.task_description:
#             return (obj.task_description[:50] + "...") if len(obj.task_description) > 50 else obj.task_description
#         return "-"
#     short_description.short_description = "Task Description"





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
