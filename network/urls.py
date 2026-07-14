from django.urls import path

from . import views

urlpatterns = [
    path("nas", views.NasDeviceListView.as_view()),
]
