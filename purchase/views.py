from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from suppliers.models import Supplier
from .models import Purchase, PurchaseItem


def _decimal(value, default="0.00"):
    try:
        return Decimal(str(value or default))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)


def generate_purchase_no():
    last_purchase = Purchase.objects.order_by("-id").first()

    if last_purchase:
        number = last_purchase.id + 1
    else:
        number = 1

    return f"PVM-PUR-{number:05d}"


def purchase_list(request):
    purchases = (
        Purchase.objects
        .select_related("supplier")
        .order_by("-purchase_date", "-id")
    )

    return render(
        request,
        "purchase/purchase_list.html",
        {"purchases": purchases},
    )


def purchase_detail(request, pk):
    purchase = get_object_or_404(
        Purchase.objects.select_related("supplier").prefetch_related("items"),
        pk=pk,
    )

    return render(
        request,
        "purchase/purchase_detail.html",
        {"purchase": purchase},
    )


@transaction.atomic
def purchase_create(request):
    suppliers = Supplier.objects.filter(active=True).order_by("name")

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        invoice_no = request.POST.get("invoice_no", "").strip()
        purchase_date = request.POST.get("purchase_date")
        discount = _decimal(request.POST.get("discount"))
        tax = _decimal(request.POST.get("tax"))
        paid_amount = _decimal(request.POST.get("paid_amount"))
        payment_method = request.POST.get("payment_method", "Cash")
        notes = request.POST.get("notes", "").strip()

        if not supplier_id:
            messages.error(request, "Please select a supplier.")
            return redirect("purchase:create")

        supplier = get_object_or_404(
            Supplier,
            pk=supplier_id,
            active=True,
        )

        item_names = request.POST.getlist("item_name[]")
        quantities = request.POST.getlist("quantity[]")
        units = request.POST.getlist("unit[]")
        rates = request.POST.getlist("rate[]")

        valid_items = []

        for item_name, quantity, unit, rate in zip(
            item_names,
            quantities,
            units,
            rates,
        ):
            item_name = item_name.strip()

            if not item_name:
                continue

            qty = _decimal(quantity)
            item_rate = _decimal(rate)

            if qty <= 0:
                continue

            if item_rate < 0:
                continue

            valid_items.append(
                {
                    "item_name": item_name,
                    "quantity": qty,
                    "unit": unit.strip() or "Nos",
                    "rate": item_rate,
                }
            )

        if not valid_items:
            messages.error(
                request,
                "Please add at least one valid purchase item.",
            )
            return redirect("purchase:create")

        purchase = Purchase.objects.create(
            purchase_no=generate_purchase_no(),
            supplier=supplier,
            invoice_no=invoice_no,
            purchase_date=purchase_date or timezone.localdate(),
            discount=discount,
            tax=tax,
            paid_amount=paid_amount,
            payment_method=payment_method,
            notes=notes,
        )

        subtotal = Decimal("0.00")

        for item_data in valid_items:
            line_total = (
                item_data["quantity"] *
                item_data["rate"]
            )

            PurchaseItem.objects.create(
                purchase=purchase,
                item_name=item_data["item_name"],
                quantity=item_data["quantity"],
                unit=item_data["unit"],
                rate=item_data["rate"],
            )

            subtotal += line_total

        purchase.subtotal = subtotal
        purchase.total = purchase.calculate_total()

        if purchase.paid_amount <= 0:
            purchase.payment_status = "Pending"
        elif purchase.paid_amount >= purchase.total:
            purchase.payment_status = "Paid"
        else:
            purchase.payment_status = "Partial"

        purchase.save()

        messages.success(
            request,
            f"Purchase {purchase.purchase_no} created successfully.",
        )

        return redirect(
            "purchase:detail",
            pk=purchase.pk,
        )

    context = {
        "suppliers": suppliers,
        "purchase_no": generate_purchase_no(),
        "today": timezone.localdate(),
    }

    return render(
        request,
        "purchase/purchase_create.html",
        context,
    )