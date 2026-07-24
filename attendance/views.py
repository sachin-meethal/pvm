from django.shortcuts import render
from .models import Attendance


def attendance_list(request):
    records = Attendance.objects.select_related("employee").all()

    return render(
        request,
        "attendance/list.html",
        {
            "records": records
        }
    )