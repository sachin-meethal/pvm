from django.db import models


class Supplier(models.Model):

    name = models.CharField(max_length=150)

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    gst_number = models.CharField(
        max_length=50,
        blank=True
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        if self.company_name:
            return f"{self.name} - {self.company_name}"

        return self.name