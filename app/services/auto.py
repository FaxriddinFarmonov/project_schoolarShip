
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
            'pr': Cited_by


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
        pagination = Model.objects.all().order_by('-pk')
        paginator = Paginator(pagination, settings.PAGINATE_BY)
        page_number = requests.GET.get("page", 1)
        paginated = paginator.get_page(page_number)


        ctx = {
            "roots": paginated,
            "pos": "list",

        }

    return render(requests, f'page/{key}.html', ctx)



@login_required(login_url='login')
def auto_form(requests, key, pk=None):

    if requests.user.ut not in  [1,2]:
        return redirect("login")

    try:
        Model = {
            "service": "Kafedra",
            "pr": "Price",
            "add_teach": "Teacher_info"

        }[key]


    except:
        return render(requests, 'base.html', {"error": 404})
    root = None
    if pk:
        root = eval(Model).objects.filter(pk=pk).first()

        if not root:
            ctx = {"error": 404}
            return render(requests, f'pages/{key}.html', ctx)

    form = eval(f"{Model}Form")(requests.POST or None,instance=root )
    if form.is_valid():
        form.save()

        if eval(f"{Model}Form") == Teacher_infoForm:
            search = GoogleSearch({
                    "engine": "google_scholar_author",
                    "author_id": requests.POST.get('teacher_id'),
                    "api_key": "c6787a50d55d9d782a5ba3f339c4b63d8ffe7a9bb21678db6e53029e63e63f91"
                  })

            result = search.get_json()
            name = result['author']['name']
            cited_by=result['cited_by']['table'][0]['citations']['all']
            since_2019c = result['cited_by']['table'][0]['citations']['since_2019']
            since_2019h = result['cited_by']['table'][1]['h_index']['since_2019']
            since_2019h10 = result['cited_by']['table'][2]['i10_index']['since_2019']
            h_index = result['cited_by']['table'][1]['h_index']['all']
            i10_index = result['cited_by']['table'][2]['i10_index']['all']

            info  = Cited_by.objects.create(
                name = name,
                citations=cited_by,
                h_index=h_index,
                i10_index=i10_index,
                since_2019c = since_2019c,
                since_2019h = since_2019h,
                since_2019h10 = since_2019h10,
                teacher_info = Teacher_info.objects.filter(teacher_id=requests.POST.get('teacher_id')).first()

            ).save()

            for i in range(len(result['cited_by']['graph'])):
                graph = Graph.objects.create(
                    citations = result['cited_by']['graph'][i]['citations'],
                    year = result['cited_by']['graph'][i]['year'],
                    teacher_info=Teacher_info.objects.filter(teacher_id=requests.POST.get('teacher_id')).first()

                ).save()


        return redirect('dashboard-auto-list', key=key)

    ctx = {
        "form": form,
        "pos": 'form',

    }



    return render(requests, f'page/{key}.html', ctx)


@login_required(login_url='sign-in')
def auto_del(requests, key, pk):

    if requests.user.ut  not in  [1,2]:
        return redirect("login")

    try:

        Model = {
            "service": Kafedra,
            "add_teach": Teacher_info

        }[key]

    except:
        return render(requests, 'base.html', {"error": 404})

    root = Model.objects.filter(pk=pk).first()

    if not root:
        ctx = {"error": 404}
        return render(requests, f'pages/{key}.html', ctx)
    root.delete()
    return redirect('dashboard-auto-list', key=key)


