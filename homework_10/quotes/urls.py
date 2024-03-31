from django.urls import path


from . import views


app_name = "quotes"


urlpatterns = [
    path("", views.main, name="main"),
    path("page/<int:page>/", views.main, name="main_page"),
    path("tag_add/", views.tag_add, name="tag_add"),
    path("quote/", views.quote, name="quote"),
    path("detail/<int:quote_id>", views.detail, name="detail"),
    path("done/<int:quote_id>", views.set_done, name="set_done"),
    path("delete/<int:quote_id>", views.delete_quote, name="delete"),
    path("author/<str:fullname>/", views.author, name="author"),
    path("add_author/", views.add_author, name="add_author"),
    path("quotes_by_tag/<str:name>/", views.tag_info, name="quotes_by_tag"),
    path("quotes_by_tag/<str:name>/page/<int:page>/", views.tag_info, name="quotes_by_tag_paginated"),
]
