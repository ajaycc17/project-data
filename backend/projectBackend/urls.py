from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("search/<str:query>/", views.search_projects, name="search_projects"),
    path("single/<str:projId>/", views.singleProject, name="singleProject"),
]
