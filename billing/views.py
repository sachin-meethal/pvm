from decimal import Decimal
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from menu.models import Category, MenuItem
from .models import Bill, BillItem


def pos(request):
    categories = Category.objects.all()
    items = MenuItem.objects.filter(available=True)

    return render(
        request,
        "billing/pos.html",
        {
            "categories": categories,
            "items": items,
        },
    )


@csrf_exempt
def save_bill(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Invalid request"},
            status=400,
        )

    data = json.loads(request.body)

    cart = data.get("cart", [])
    customer = data.get("customer_name", "")
    payment = data.get("payment_method", "Cash")

    last_bill = Bill.objects.order_by("-id").first()

    if last_bill:
        number = int(last_bill.bill_no.replace("PVM", "")) + 1
    else:
        number = 1

    bill_no = f"PVM{number:06d}"

    total = Decimal("0.00")

    bill = Bill.objects.create(
        bill_no=bill_no,
        customer_name=customer,
        payment_method=payment,
        total=0,
    )

    for row in cart:
        item = MenuItem.objects.get(id=row["id"])

        qty = int(row["qty"])
        price = item.price
        line_total = price * qty

        BillItem.objects.create(
            bill=bill,
            item=item,
            quantity=qty,
            price=price,
            total=line_total,
        )

        total += line_total

    bill.total = total
    bill.save()

    return JsonResponse(
        {
            "status": "success",
            "bill_no": bill.bill_no,
            "total": str(total),
        }
    )
from django.shortcuts import render
from .models import Bill


def bill_history(request):
    bills = Bill.objects.order_by("-created_at")

    return render(
        request,
        "billing/history.html",
        {
            "bills": bills,
        },
    )
from django.shortcuts import get_object_or_404

def receipt(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    return render(
        request,
        "billing/receipt.html",
        {
            "bill": bill,
        },
    )