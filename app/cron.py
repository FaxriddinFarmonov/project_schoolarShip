from app.models.doctor import Teacher_info,Graph,Cited_by
import random
from django.db import  connection
from serpapi import GoogleSearch



def scholar_cron():
    try:
        cited_by = Cited_by.objects.all().delete()
        graph = Graph.objects.all().delete()
    except :
        pass

    teach_info = Teacher_info.objects.all()

    for i in teach_info:
        search = GoogleSearch({
            "engine": "google_scholar_author",
            "author_id": i.teacher_id,
            "api_key": "c6787a50d55d9d782a5ba3f339c4b63d8ffe7a9bb21678db6e53029e63e63f91"
        })
        result = search.get_json()

        name = result['author']['name']
        cited_by = result['cited_by']['table'][0]['citations']['all']
        since_2019c = result['cited_by']['table'][0]['citations']['since_2019']
        since_2019h = result['cited_by']['table'][1]['h_index']['since_2019']
        since_2019h10 = result['cited_by']['table'][2]['i10_index']['since_2019']
        h_index = result['cited_by']['table'][1]['h_index']['all']
        i10_index = result['cited_by']['table'][2]['i10_index']['all']

        info = Cited_by.objects.create(
            name=name,
            citations=cited_by,
            h_index=h_index,
            i10_index=i10_index,
            since_2019c=since_2019c,
            since_2019h=since_2019h,
            since_2019h10=since_2019h10,
            teacher_info=Teacher_info.objects.filter(teacher_id=i.teacher_id)

        ).save()

        for j in range(len(result['articles'])):
            Graph.objects.create(
                title=result['articles'][j]['title'],
                value=result['articles'][j]['cited_by']['value'],
                year=result['articles'][j]['year'],
                teacher_info=Teacher_info.objects.filter(teacher_id=i.teacher_id).first(),

            ).save()



