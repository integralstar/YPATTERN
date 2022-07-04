from django.urls import path
from .views import *

app_name = "checker"

urlpatterns = [
    path("", CheckerListView.as_view(), name='list'),
    path("URL/", URLClassifier, name="URLClassifier"),
    path("MyURL/", MyURLClassifier, name="MyURLClassifier"),
    path("search/", SearchFormView.as_view(), name="search"),
    path("add/", CheckerCreateView.as_view(), name='add'),
    path("detail/<int:pk>/", CheckerDetailView.as_view(), name='detail'),
    path("update/<int:pk>", CheckerUpdateView.as_view(), name='update'),
    path("delete/<int:pk>", CheckerDeleteView.as_view(), name='delete'),
    path("mychecker", MyChecker, name='mychecker'),
]
