from django.db import models
from menu.models import MenuItem


class Bill(models.Model):
    PAYMENT_METHOD = [
        ("Cash", "Cash"),
        ("Card", "Card"),
        ("UPI", "UPI"),
    ]

    bill_no = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bill_no


class BillItem(models.Model):
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bill.bill_no} - {self.item.name}"