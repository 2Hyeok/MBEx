from django.urls.conf import path
from board import views

app_name = "board"

urlpatterns = [
    path("list", views.ListView.as_view(), name="list" ),
    path("write", views.WriteView.as_view(), name="write" ),
    path("detail", views.DetailView.as_view(), name="detail" ),
    ]