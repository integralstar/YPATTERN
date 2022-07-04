from django.urls import path
from .views import *

app_name = "PM"

urlpatterns = [
    path("", index, name='index'),
    path("pattern", get_pattern, name='get_pattern'),
]
