from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    EMPLOYEE_TYPE = (
        ("Daily", "Daily Wage"),
        ("Monthly", "Monthly Salary"),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)

    employee_id = models.CharField(max_length=20, unique=True)

    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    designation = models.CharField(max_length=100)

    salary_type = models.CharField(
        max_length=20,
        choices=EMPLOYEE_TYPE,
        default="Monthly",
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    joining_date = models.DateField()

    active = models.BooleanField(default=True)

    photo = models.ImageField(
        upload_to="employees/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.employee_id} - {self.first_name}"