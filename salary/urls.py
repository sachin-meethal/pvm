from django.urls import path

from . import views


urlpatterns = [
    path("", views.salary_list, name="salary_list"),
    path("add/", views.add_salary, name="add_salary"),
]