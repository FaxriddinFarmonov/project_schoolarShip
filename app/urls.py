from django.shortcuts import render
from django.urls import path

from app.bank_services.link_schot import contract_update_view
from .bank_services.card_information_exel import export_all_cardinfo_zip
from .bank_services.doctor import translate_document_view
from .bank_services.get_information import card_lookup_view
from .bank_services.get_terminals import terminal_lookup_view
from .bank_services.limit_card import send_card_restriction
from .bank_services.parse_file import export_cashwithdrawal_from_zip
from .bank_services.read_terminal import read_terminal_view
from .bank_services.read_terminal_exel import export_terminal_to_excel_flat_address
from .bank_services.remove_limit import remove_limit
from .bank_services.terminal_information_exel import export_terminalinfo_to_excel
from .bank_services.upload_file import upload_file_view
from .services.auto import gets, auto_del, get_fak, card_block, active_card_status, payment_status, get_customers, \
    get_file, get_card_information, get_terminal_information, read_terminal_information, get_limit_card
from .services.auth import profile,sign_up,sign_in,sign_out,search,otp,resent_otp
from .services.client import client_doc
from .services.derector import list_members,banned,grader
# from .services.get_balance import get_balance_view
# from .export_exel import export_data_to_excel,export_data_to_excel_fak,export_scopus_to_excel,export_merged_data_to_excel
from .views import index,  balance_update_view
from app.bank_services.create_customer_view import subject_update_view
from app.bank_services.get_schot import get_schot
from app.bank_services.active_card import activate_card
from app.bank_services.block_card import block_card_view
from app.bank_services.get_balance import get_balance_view
from django.conf import settings
from django.conf.urls.static import static


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
    path("auto/",get_fak,name="get_cardbalance" ),
    path("card_block/",card_block,name="card_block" ),
    path("active_card_status/",active_card_status,name="active_card_status" ),
    path('activate-card/', activate_card, name='activate_card'),
    path('contract_update_view/', contract_update_view, name='contract_update_view'),


    path("exportterminal-info/", export_terminalinfo_to_excel, name="export_terminal_info"),
    path('upload/', upload_file_view, name='upload_file'),
    path('send_card_restriction/', send_card_restriction, name='send_card_restriction'),
    path('remove_limit/', remove_limit, name='remove_limit'),
    path('terminal_information/', terminal_lookup_view, name='terminal_information'),
    path('read_terminal_information/', read_terminal_information, name='read_terminal_information'),
    path("export-terminal/<int:pk>/", export_terminal_to_excel_flat_address, name="export_terminal"),
    path('read_terminal_view/', read_terminal_view, name='read_terminal_view'),
    path('upload/success/', lambda request: render(request, 'success.html'), name='file_upload_success'),


    path('payment_status/', payment_status, name='payment_status'),
    path('get_schot/', get_schot, name='get_schot'),
    path('get_limit_card/', get_limit_card, name='get_limit_card'),
    path('get_customers/', get_customers, name='get_customers'),
    path('get_file/', get_file, name='get_file'),
    path('SubjectUpdate/', subject_update_view, name='subject_update_view'),
    path('get_card/', card_lookup_view, name='card_lookup_view'),
    path('get_card_information/', get_card_information, name='get_card_information'),
    path('get_terminal_information/', get_terminal_information, name='get_terminal_information'),

    path("auto/<key>/detail/<int:pk>/",gets,name="dashboard-auto-detail" ),


    # path("auto/<key>/add/",auto_form,name="dashboard-auto-add" ),
    # path("auto/add/",auto_form,name="dashboard-auto-add" ),



    path("translate/<int:doc_id>/", translate_document_view, name="translate_document"),
    path('get_balance/', get_balance_view, name='get_balance_view'),
    path('block-card/', block_card_view, name='block_card'),
    path('payment-card/', balance_update_view, name='payment_card'),

    path('export_cashwithdrawal_from_file/<int:file_id>/', export_cashwithdrawal_from_zip, name='export_cashwithdrawal_from_file'),
    path('export_zip/', export_all_cardinfo_zip, name='export_zip'),

    path("auto/<key>/del/<int:pk>/",auto_del,name="dashboard-auto-delete" ),

    # path("auto/<key>/edit/<int:pk>/",auto_form,name="dashboard-auto-edit" ),

    # path("get_balance/",get_balance_view,name="get_balance" )
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
    #path("search_results/",search_results,name="search_results"),

    #client
    path("client/doc/<int:service>/",client_doc,name='servicedocs')

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
