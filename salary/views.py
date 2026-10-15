from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from employees.models import Employee
from .models import Salary


def salary_list(request):
    salaries = Salary.objects.select_related("employee").order_by("-salary_month", "-id")

    return render(
        request,
        "salary/salary_list.html",
        {
            "salaries": salaries,
        },
    )


def add_salary(request):
    employees = Employee.objects.filter(active=True).order_by("first_name")

    if request.method == "POST":
        employee_id = request.POST.get("employee")
        salary_month = request.POST.get("salary_month")
        salary_type = request.POST.get("salary_type", "Monthly")

        basic_salary = request.POST.get("basic_salary") or 0
        working_days = request.POST.get("working_days") or 0
        present_days = request.POST.get("present_days") or 0
        overtime_hours = request.POST.get("overtime_hours") or 0
        overtime_amount = request.POST.get("overtime_amount") or 0
        advance = request.POST.get("advance") or 0
        deduction = request.POST.get("deduction") or 0

        payment_status = request.POST.get("payment_status", "Pending")
        payment_date = request.POST.get("payment_date") or None
        payment_method = request.POST.get("payment_method", "Cash")
        notes = request.POST.get("notes", "")

        employee = get_object_or_404(Employee, id=employee_id)

        Salary.objects.create(
            employee=employee,
            salary_month=salary_month,
            salary_type=salary_type,
            basic_salary=basic_salary,
            working_days=working_days,
            present_days=present_days,
            overtime_hours=overtime_hours,
            overtime_amount=overtime_amount,
            advance=advance,
            deduction=deduction,
            payment_status=payment_status,
            payment_date=payment_date,
            payment_method=payment_method,
            notes=notes,
        )

        messages.success(
            request,
            f"Salary added successfully for {employee}."
        )

        return redirect("salary_list")

    return render(
        request,
        "salary/add_salary.html",
        {
            "employees": employees,
        },
    )