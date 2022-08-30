from django.urls.conf import path
from django.views.generic.base import TemplateView
from member import views

# templates -> 클래스 뷰를 따로 만들지 않겠다는뜻임
urlpatterns = [
    path("main", views.MainView.as_view(), name="main"),
    path("write", views.WriteView.as_view(), name="write"),
    path("confirm", views.ConfirmView.as_view(),name="confirm"),
    path("login", views.LoginView.as_view(),name="login"),
    path("logout", views.LogoutView.as_view(),name="logout"),
    path("delete", views.DeleteView.as_view(),name="delete"),
    path("modify", views.ModifyView.as_view(),name="modify"),
    path("modifypro", views.ModifyProView.as_view(),name="modifypro"),
    ]

# main 처럼 생성하면 views 에 만들어줄 필요 없음