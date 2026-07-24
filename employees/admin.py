from django.contrib import admin
from .models import Employee, Department


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "first_name",
        "phone",
        "department",
        "salary",
        "active",
    )

    search_fields = (
        "employee_id",
        "first_name",
        "phone",
    )


admin.site.register(Department)