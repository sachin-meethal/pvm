from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import render

from billing.models import Bill
from employees.models import Employee


@login_required
def dashboard(request):

    today = date.today()

    today_bills = Bill.objects.filter(created_at__date=today)

    today_sales = (
        today_bills.aggregate(total=Sum("total"))["total"] or 0
    )

    total_orders = today_bills.count()

    employees = Employee.objects.count()

    context = {
        "today_sales": today_sales,
        "orders": total_orders,
        "employees": employees,
        "purchase": 0,   # We'll connect this later
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )