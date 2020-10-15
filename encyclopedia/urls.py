from django.urls import path

from . import views

# app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    # path("<str:entry_id>", views.detail, name="detail")
]
