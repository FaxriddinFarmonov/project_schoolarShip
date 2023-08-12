from django.urls import path

from .services.auto import gets, auto_form, auto_del
from .views import index

urlpatterns = [
    path("", index, name="home"),

    #auto

    path("auto/<key>/",gets,name="dashboard-auto-list" ),
    path("auto/<key>/detail/<int:pk>/",gets,name="dashboard-auto-detail" ),
    path("auto/<key>/add/",auto_form,name="dashboard-auto-add" ),
    path("auto/<key>/edit/<int:pk>/",auto_form,name="dashboard-auto-edit" ),
    path("auto/<key>/del/<int:pk>/",auto_del,name="dashboard-auto-delete" ),

]
