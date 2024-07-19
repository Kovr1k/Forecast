from django.urls import path, include
from .views import *

urlpatterns = [
    path("", Main.as_view(), name="main"),
]