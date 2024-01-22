import datetime
from contextlib import closing
from django.conf import settings
from django.contrib.auth import logout
from django.db import connection
from django.shortcuts import redirect,render
from methodism import dictfetchone
from app.models.doctor import Spam,Kafedra
from app.models.books import Books
import random
from django.db import  connection


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

def my_scheduled_job():
     number = random.randint(2,1000)
     book= Books.objects.create(
          number=number
      )
     book.save()







def sektion(request):
    model = Kafedra.objects.all()
    ctx = {
        'professions':model
    }

    return ctx