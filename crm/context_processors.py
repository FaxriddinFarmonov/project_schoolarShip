import datetime
from contextlib import closing
from django.conf import settings
from django.contrib.auth import logout
from django.db import connection
from django.shortcuts import redirect,render
from methodism import dictfetchone
from app.models.doctor import Spam, Kafedra
from serpapi import GoogleSearch
# Teacher_info, Teacher_scopus, Cited_by, Graph

def user_type(request):
   try:

       types = {
            1: "page/direct/main.html",
            2: "page/admin/main.html",
            3: "page/doc/main.html",
            4: "page/client/main.html"
       }.get(request.user.ut, "page/doc/main.html")
   except:
        types = "page/doc/main.html"

   ctx = {
       "type":types,
       "app_name":settings.APP_NAME
   }
   if not request.user.is_anonymous:
        ctx.update({'ut':request.user.ut})
   return ctx


def count(request):

   sql = """
   select(select COUNT(*)from app_user where ut = 3 ) as cnt_doc,
   (select COUNT( *)  from app_user where ut = 2 ) as cnt_admin,
   (select COUNT( *) from app_user where ut = 4 ) as cnt_client,
   (select COUNT( *)  from app_kafedra ) as cnt_service
   from django_session limit 1   
   """



   with closing(connection.cursor()) as cursor:
       cursor.execute(sql)
       result = dictfetchone(cursor)

   return {
       "count": result
   }

# def check_spam(request):
#     spam_user = Spam.objects.filter(user_id=request.user.id,active=True ).first()
#
#     if spam_user:
#         if (spam_user.date-datetime.datetime.now()).total_seconds()>300:
#             spam_user.active = False
#             spam_user.user.is_spam = False
#             spam_user.user.save()
#             spam_user.save()
#             return {'spam':False,"spam_user":{}}
#         return  {'spam':True,"spam_user":spam_user}
#     return {'spam':False,"spam_user":{}}
#

from app.models.books import Books
import random
# from django.db import  connection






# def hello(request):
#     datas = Teacher_info.objects.all().first()
#     # print(datas.datetime.datetime)
#     # if (datetime.datetime.now() - data.created).total_seconds() >= 100:
#     #     try:
#     #         cited_by = Cited_by.objects.all().delete()
#     #         graph = Graph.objects.all().delete()
#     #     except:
#     #         pass
#     #
#     #     teach_info = Teacher_info.objects.all()
#     #
#     #     for i in teach_info:
#     #         search = GoogleSearch({
#     #             "engine": "google_scholar_author",
#     #             "author_id": i.teacher_id,
#     #             "api_key": "8a781032fba81c6826c0f57bf96ada4883e4b6ba8ce5b5c775c57323108b0d00"
#     #         })
#     #         result = search.get_json()
#     #
#     #         name = result['author']['name']
#     #         cited_by = result['cited_by']['table'][0]['citations']['all']
#     #         since_2019c = result['cited_by']['table'][0]['citations']['since_2019']
#     #         since_2019h = result['cited_by']['table'][1]['h_index']['since_2019']
#     #         since_2019h10 = result['cited_by']['table'][2]['i10_index']['since_2019']
#     #         h_index = result['cited_by']['table'][1]['h_index']['all']
#     #         i10_index = result['cited_by']['table'][2]['i10_index']['all']
#     #
#     #         info = Cited_by.objects.create(
#     #             name=name,
#     #             citations=cited_by,
#     #             h_index=h_index,
#     #             i10_index=i10_index,
#     #             since_2019c=since_2019c,
#     #             since_2019h=since_2019h,
#     #             since_2019h10=since_2019h10,
#     #             teacher_info=Teacher_info.objects.filter(teacher_id=i.teacher_id).first()
#     #
#     #         ).save()
#     #
#     #         for j in range(len(result['articles'])):
#     #             if result['articles'][i]['cited_by'] is not None and 'publication' in result['articles'][i] and \
#     #                     result['articles'][i]['publication'] is not None:
#     #                 Graph.objects.create(
#     #                     name=name,
#     #                     title=result['articles'][j]['title'],
#     #                     value=result['articles'][j]['cited_by']['value'],
#     #                     year=result['articles'][j]['year'],
#     #                     teacher_info=Teacher_info.objects.filter(teacher_id=i.teacher_id).first(),
#     #                     links=result['articles'][j]['link'],
#     #
#     #                 ).save()
#     ctx = {
#             'a':'name'
#         }
#     return ctx
#
def sektion(request):
    model = Kafedra.objects.all()
    ctx = {
        'professions':model
    }

    return ctx