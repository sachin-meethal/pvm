from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    context = {
        "today_sales": 0,
        "orders": 0,
        "employees": 0,
        "purchase": 0,
    }
    return render(request, "dashboard/dashboard.html", context)