
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("MANAGER", "Manager"),
        ("CASHIER", "Cashier"),
        ("KITCHEN", "Kitchen"),
        ("STORE", "Store Keeper"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CASHIER")
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.username