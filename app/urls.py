from django.urls import path

from .services.auto import gets, auto_form, auto_del,get_fak
from .services.auth import profile,sign_up,sign_in,sign_out,search,otp,resent_otp
from .services.client import client_doc
from .services.derector import list_members,banned,grader
from .export_exel import export_data_to_excel,export_data_to_excel_fak
from .views import index,search_results



urlpatterns = [

    path("", index, name="home"),
    path('otp/',otp ,name='otp'),
    path('resent_otp/',resent_otp ,name='resent_otp'),


    # user
    path("auth/",sign_in, name="login"),
    path("auto/regis/", sign_up, name="regis"),
    path("auto/logout/", sign_out, name="logout"),
    path("auto/profile/", profile, name="profile"),

    #auto
    path("auto/<key>/",gets,name="dashboard-auto-list" ),
    path("au/<key>/",get_fak,name="get_fak" ),
    path("auto/<key>/detail/<int:pk>/",gets,name="dashboard-auto-detail" ),
    path("auto/<key>/add/",auto_form,name="dashboard-auto-add" ),
    path("auto/<key>/edit/<int:pk>/",auto_form,name="dashboard-auto-edit" ),
    path("auto/<key>/del/<int:pk>/",auto_del,name="dashboard-auto-delete" ),

    #member
    path("export_data_to_excel/<key>/", export_data_to_excel, name='export_data_excel'),
    path("export_data_to_excel_fak/<key>/", export_data_to_excel_fak, name='export_data_to_excel_fak'),
    path("member/<int:tpe>/",list_members,name='members'),
    path("member/new/<int:new>/",list_members,name='members-new'),
    path("banner/u-<int:user_id>/t-<int:tpe>/s-<int:status>/",banned,name='banned'),
    path("grader/<int:pk>/<int:ut>/<int:dut>/",grader,name='grader'),
    # path("spammer/<int:pk>/<int:dut>/",spammer,name='spammer'),

    #search
    path("search_results/",search_results,name="search_results"),

    #client
    path("client/doc/<int:service>/",client_doc,name='servicedocs')


]
