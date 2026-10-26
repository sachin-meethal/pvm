from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Supplier


def supplier_list(request):
    suppliers = Supplier.objects.all().order_by("name")

    return render(
        request,
        "suppliers/supplier_list.html",
        {"suppliers": suppliers},
    )


def supplier_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        company_name = request.POST.get("company_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()
        gst_number = request.POST.get("gst_number", "").strip()
        opening_balance = request.POST.get("opening_balance") or 0

        if not name:
            messages.error(request, "Supplier name is required.")
            return redirect("suppliers:create")

        if not phone:
            messages.error(request, "Phone number is required.")
            return redirect("suppliers:create")

        Supplier.objects.create(
            name=name,
            company_name=company_name,
            phone=phone,
            email=email,
            address=address,
            gst_number=gst_number,
            opening_balance=opening_balance,
            active=True,
        )

        messages.success(
            request,
            "Supplier added successfully."
        )

        return redirect("suppliers:list")

    return render(
        request,
        "suppliers/supplier_form.html"
    )


def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":
        supplier.name = request.POST.get("name", "").strip()
        supplier.company_name = request.POST.get(
            "company_name", ""
        ).strip()
        supplier.phone = request.POST.get("phone", "").strip()
        supplier.email = request.POST.get("email", "").strip()
        supplier.address = request.POST.get("address", "").strip()
        supplier.gst_number = request.POST.get(
            "gst_number", ""
        ).strip()

        supplier.opening_balance = (
            request.POST.get("opening_balance") or 0
        )

        supplier.active = (
            request.POST.get("active") == "on"
        )

        supplier.save()

        messages.success(
            request,
            "Supplier updated successfully."
        )

        return redirect("suppliers:list")

    return render(
        request,
        "suppliers/supplier_form.html",
        {"supplier": supplier},
    )