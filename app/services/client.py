import datetime
from contextlib import closing

from django.db import connection
from methodism import dictfetchall

from app.models import Kafedra,User
from django.shortcuts import render,redirect

def skorost(funksiya):
    def wrapper(*args,**kwargs):
        start = datetime.datetime.now()
        a = funksiya(*args,**kwargs)
        end = datetime.datetime.now()
        print('>>>>', start)
        print('<<<<', end)
        return a
    return  wrapper
@skorost
def client_doc(request,service:int = None):
    # sql=f"""
    # select cr.id as cr_id, cr.name as cr_name, doc.id, doc.name as fname, doc.familya as lname, doc.img,doc.phone,doc.gender,
    # pro.name as prof, pos.name as 'position'
    # from app_service as cr
    # inner join app_servicedoc sd on sd.service_id=cr.id
    # inner join app_user doc on sd.doc_id=doc.id
    # left join app_position pos on pos.id=doc.position_id
    # left join app_professions pro on pro.id=doc.prof_id
    # where cr.id={ service }
    #
    # """
    #
    # with closing(connection.cursor()) as cursor:
    #     cursor.execute(sql)
    #     result = dictfetchall(cursor)

    result = User.objects.filter(prof_id=service)

    ctx = {
        "roots" : result,
    }

    return render(request,'page/client/client_doc.html',ctx)

