from django.urls import path
from . import views


app_name = "quotes"


urlpatterns = [
    path("", views.main, name="main"),
    path("tag/", views.tag, name="tag"),
    path("quote/", views.quote, name="quote"),
    path("detail/<int:quote_id>", views.detail, name="detail"),
    path("done/<int:quote_id>", views.set_done, name="set_done"),
    path("delete/<int:quote_id>", views.delete_quote, name="delete"),
    path("author/<str:fullname>/", views.author, name="author"),
]
