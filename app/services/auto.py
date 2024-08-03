import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from app.models import *
from app.forms import *
from serpapi import GoogleSearch
from pprint import pprint
from app.models.doctor import Kafedra



@login_required(login_url='login')
def gets(requests, key, pk=None):

    if requests.user.ut not in  [1,2]:
        return redirect("login")
    try:
        Model = {
            "service": Kafedra,
            "add_teach" : Teacher_info,
            'pr': Cited_by,
            'scopus_pr': Cited_by_Scopus,
            'scopus': Teacher_scopus,



        }[key]
    except:
        return render(requests, 'base.html', {"error": 404})
    if pk:
        root = Model.objects.filter(pk=pk).first()

        ctx = {
            "pos": "one",
            'root': root,
           
        }
        
        if not root:
            ctx['error'] = 404
    else:
        pagination = Model.objects.filter().order_by('-pk')
        paginator = Paginator(pagination, settings.PAGINATE_BY)
        page_number = requests.GET.get("page", 1)
        paginated = paginator.get_page(page_number)


        ctx = {
            "roots": paginated,
            "pos": "list",
            'key' :key
            
            

        }
        k = Model.objects.filter(id=1).first()
    return render(requests, f'page/{key}.html', ctx)



@login_required(login_url='login')
def auto_form(request, key, pk=None):

    if request.user.ut not in  [1,2]:
        return redirect("login")

    try:
        Model = {
            "service": "Kafedra",
            "pr": "Price",
            "add_teach": "Teacher_info",
            "scopus": "Teacher_scopus"

        }[key]


    except:
        return render(request, 'base.html', {"error": 404})
    root = None
    if pk:
        root = eval(Model).objects.filter(pk=pk).first()

        if not root:
            ctx = {"error": 404}
            return render(request, f'pages/{key}.html', ctx)

    form = eval(f"{Model}Form")(request.POST or None,instance=root )
    if form.is_valid():
        form.save()

        if eval(f"{Model}Form") == Teacher_infoForm:

            search = GoogleSearch({
                    "engine": "google_scholar_author",
                    "author_id": request.POST.get('teacher_id_scholar'),
                    "api_key": "acca4dcb415645c1b19ed5cc6ba845fb2df00b00925bb1545d4005f842030f46"
                  })
            result = search.get_json()
            print(result)

            name =result['author']['name']
            autor_id =result['search_parameters']['author_id']
            cited_by=result['cited_by']['table'][0]['citations']['all']
            since_2019c = result['cited_by']['table'][0]['citations']['since_2019']
            since_2019h = result['cited_by']['table'][1]['h_index']['since_2019']
            since_2019h10 = result['cited_by']['table'][2]['i10_index']['since_2019']
            h_index = result['cited_by']['table'][1]['h_index']['all']
            i10_index = result['cited_by']['table'][2]['i10_index']['all']
            Teacher_info.objects.filter(teacher_id_scholar=autor_id).update(name=name)

            info  = Cited_by.objects.create(
                name = name,
                citations=cited_by,
                h_index=h_index,
                i10_index=i10_index,
                since_2019c = since_2019c,
                since_2019h = since_2019h,
                since_2019h10 = since_2019h10,
                teacher_info = Teacher_info.objects.filter(teacher_id_scholar=request.POST.get('teacher_id_scholar')).first(),

            ).save()

            for i in range(len(result['articles'])):
                if result['articles'][i]['cited_by']['value'] is not None and 'publication' in result['articles'][i] and \
                        result['articles'][i]['publication'] is not None:
                    Graph.objects.create(
                        name=name,
                        title = result['articles'][i]['title'],
                        value = result['articles'][i]['cited_by']['value'],
                        year = result['articles'][i]['year'],
                        links= result['articles'][i]['link'],
                        publication= result['articles'][i]['publication'][0:-6],
                        teacher_info = Teacher_info.objects.filter(teacher_id_scholar=request.POST.get('teacher_id_scholar')).first(),


                    ).save()
        elif eval(f"{Model}Form") == Teacher_scopusForm:

            url = 'https://api.elsevier.com/content/search/scopus'
            link = 'https://www.scopus.com/authid/detail.uri?authorId='
            author_id =  request.POST.get('teacher_id_scopus')
            count = 0

            headers = {
                'X-ELS-APIKey': '285fbb82ea7717b8bc6b7e0f9d2b422d',
            }
            params = {
                'query': f'AU-ID({author_id})',
                'count': 'all'
            }
            print()
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            for j in range(len(data['search-results']['entry'])):
                if 'citedby-count' in data['search-results']['entry'][j] and data['search-results']['entry'][j]['citedby-count'] is not '0':
                    count = count + int(data['search-results']['entry'][j]['citedby-count'])
                    Graph_Scoupus.objects.create(
                        name= request.POST.get('name'),
                        title =data['search-results']['entry'][j]['dc:title'],
                        value = data['search-results']['entry'][j]['citedby-count'],
                        publication = data['search-results']['entry'][j]['prism:publicationName'],
                        year = data['search-results']['entry'][j]['prism:coverDate'][0:4],
                        links = f" {link}{author_id}",
                        teacher_scopus =  Teacher_scopus.objects.filter(teacher_id_scopus=author_id).first(),

                    ).save()
            Cited_by_Scopus.objects.create(
                name=request.POST.get('name'),
                citations = count,
                publications = len(data['search-results']['entry']),
                teacher_scopus=Teacher_scopus.objects.filter(
                teacher_id_scopus=request.POST.get('teacher_id_scopus')).first(),

            )

        return redirect('dashboard-auto-list', key=key)

    ctx = {
        "form": form,
        "pos": 'form',

    }



    return render(request, f'page/{key}.html', ctx)


@login_required(login_url='sign-in')
def auto_del(requests, key, pk):

    if requests.user.ut  not in  [1,2]:
        return redirect("login")

    try:

        Model = {
            "service": Kafedra,
            "add_teach": Teacher_info,
            'scopus':Teacher_scopus

        }[key]

    except:
        return render(requests, 'base.html', {"error": 404})

    root = Model.objects.filter(pk=pk).first()

    if not root:
        ctx = {"error": 404}
        return render(requests, f'pages/{key}.html', ctx)
    root.delete()
    return redirect('dashboard-auto-list', key=key)


# @login_required(login_url='login')
# def get_fak(request,key):
#     try:
#         model = Cited_by.objects.filter(teacher_info__kafedra__name=key)
#         print(model)
#     except:
#         return render(request, f'page/pr.html', {"error": 404})
#     ctx = {
#         'roots' : model,
#         'key':key
#
#     }
#     return render(request, f'page/pr.html', ctx)


def get_fak(request,key):
    try:
        # Birinchi ma'lumotlar bazasidan ma'lumotlarni olish
        model1 = Cited_by.objects.filter(teacher_info__kafedra__name=key)

        # Ikkinchi ma'lumotlar bazasidan ma'lumotlarni olish
        model2 = Cited_by_Scopus.objects.filter(teacher_scopus__kafedra__name=key)

        # Ma'lumotlarni tekislaymiz va ularni bitta ro'yxatga qo'shamiz

        # Foydalanuvchiga ma'lumotlarni ko'rsatish
        ctx = {
           'roots' : model1,
           'roots2' : model2,

            'key': key
        }
        return render(request, 'page/pr.html', ctx)
    except:
        return render(request, 'page/pr.html', {"error": 404})
