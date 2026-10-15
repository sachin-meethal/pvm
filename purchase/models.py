from decimal import Decimal

from django.db import models

from suppliers.models import Supplier


class Purchase(models.Model):

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Partial", "Partial"),
    ]

    PAYMENT_METHOD = [
        ("Cash", "Cash"),
        ("Bank", "Bank"),
        ("UPI", "UPI"),
        ("Credit", "Credit"),
    ]

    purchase_no = models.CharField(
        max_length=30,
        unique=True
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchases"
    )

    invoice_no = models.CharField(
        max_length=100,
        blank=True
    )

    purchase_date = models.DateField()

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD,
        default="Cash"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def calculate_total(self):
        total = self.subtotal + self.tax - self.discount

        if total < 0:
            total = Decimal("0.00")

        return total

    def save(self, *args, **kwargs):
        self.total = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.purchase_no


class PurchaseItem(models.Model):

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item_name = models.CharField(
        max_length=200
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=30,
        default="Nos"
    )

    rate = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_name} - {self.quantity} {self.unit}"