from django.shortcuts import render
from menu.models import Category, MenuItem


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