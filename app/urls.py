from django.urls import path

from .services.auto import gets, auto_del, get_fak, card_block, active_card_status, payment_status
from .services.auth import profile,sign_up,sign_in,sign_out,search,otp,resent_otp
from .services.client import client_doc
from .services.derector import list_members,banned,grader
# from .services.get_balance import get_balance_view
# from .export_exel import export_data_to_excel,export_data_to_excel_fak,export_scopus_to_excel,export_merged_data_to_excel
from .views import index, get_balance_view, block_card_view, activate_card, balance_update_view
from app.bank_services.create_customer_view import subject_update_view


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
    path("auto/",get_fak,name="get_fak" ),
    path("card_block/",card_block,name="card_block" ),
    path("active_card_status/",active_card_status,name="active_card_status" ),
    path('activate-card/', activate_card, name='activate_card'),
    path('payment_status/', payment_status, name='payment_status'),
    path('SubjectUpdate/', subject_update_view, name='subject_update_view'),

    path("auto/<key>/detail/<int:pk>/",gets,name="dashboard-auto-detail" ),
    # path("auto/<key>/add/",auto_form,name="dashboard-auto-add" ),
    # path("auto/add/",auto_form,name="dashboard-auto-add" ),



    path('get_balance/', get_balance_view, name='dashboard-auto-add'),
    path('block-card/', block_card_view, name='block_card'),
    path('payment-card/', balance_update_view, name='payment_card'),

    # path("auto/<key>/edit/<int:pk>/",auto_form,name="dashboard-auto-edit" ),
    path("auto/<key>/del/<int:pk>/",auto_del,name="dashboard-auto-delete" ),


    # path("get_balance/",get_balance_view,name="get_balance" ),


    #member
    # path("export_data_to_excel/<key>/", export_data_to_excel, name='export_data_excel'),
    # path("export_scopus_to_excel/<key>/", export_scopus_to_excel, name='export_scopus_to_excel'),
    # path("export_data_to_excel_fak/<key>/", export_data_to_excel_fak, name='export_data_to_excel_fak'),
    # path("export_merged_data_to_excel/<key>/", export_merged_data_to_excel, name='export_merged_data_to_excel'),


    path("member/<int:tpe>/",list_members,name='members'),
    path("member/new/<int:new>/",list_members,name='members-new'),
    path("banner/u-<int:user_id>/t-<int:tpe>/s-<int:status>/",banned,name='banned'),
    path("grader/<int:pk>/<int:ut>/<int:dut>/",grader,name='grader'),
    # path("spammer/<int:pk>/<int:dut>/",spammer,name='spammer'),

    #search
    # path("search_results/",search_results,name="search_results"),

    #client
    path("client/doc/<int:service>/",client_doc,name='servicedocs')

]
