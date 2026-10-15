from django.urls import path
from . import views

urlpatterns = [
    path("", views.pos, name="pos"),
    path("save/", views.save_bill, name="save_bill"),
    path("history/", views.bill_history, name="bill_history"),
    path("receipt/<int:bill_id>/", views.receipt, name="receipt"),
]