from django.urls.conf import path
from board import views

app_name = "board"

urlpatterns = [
    path("list", views.ListView.as_view(), name="list" ),
    path("write", views.WriteView.as_view(), name="write" ),
    path("detail", views.DetailView.as_view(), name="detail" ),
    path("delete", views.DeleteView.as_view(), name="delete" ),
    path("modify", views.ModifyView.as_view(), name="modify" ),
    path("modifypro", views.ModifyProView.as_view(), name="modifypro" ),
    path("image", views.ImageView.as_view(), name="image"),
    path("imagedown", views.ImageDown.as_view(), name="imagedown"),
    ]