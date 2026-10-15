from decimal import Decimal

from django.db import models

from employees.models import Employee


class Salary(models.Model):
    SALARY_TYPE = [
        ("Monthly", "Monthly"),
        ("Daily", "Daily"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
    ]

    PAYMENT_METHOD = [
        ("Cash", "Cash"),
        ("Bank", "Bank"),
        ("UPI", "UPI"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="salaries"
    )

    salary_month = models.DateField()

    salary_type = models.CharField(
        max_length=20,
        choices=SALARY_TYPE,
        default="Monthly"
    )

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    working_days = models.PositiveIntegerField(default=0)

    present_days = models.PositiveIntegerField(default=0)

    overtime_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00")
    )

    overtime_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    advance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    payment_date = models.DateField(
        blank=True,
        null=True
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

    def calculate_net_salary(self):
        salary = self.basic_salary + self.overtime_amount
        salary -= self.advance
        salary -= self.deduction

        if salary < 0:
            salary = Decimal("0.00")

        return salary

    def save(self, *args, **kwargs):
        self.net_salary = self.calculate_net_salary()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} - {self.salary_month:%B %Y}"