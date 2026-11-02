from django.contrib import admin
from django.urls import path
from packing import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("recommend/", views.recommend, name="recommend"),
]
