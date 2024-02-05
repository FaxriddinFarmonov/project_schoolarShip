from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.models import Kafedra
from app.models.doctor import Cited_by
from app.services.derector import notifis


# Create your views here.
@login_required(login_url='login')
def index(request):
    service = Kafedra.objects.all()
    ctx = {
        "services": service
    }
    if request.user.ut == 1:
        ctx.update(notifis())
    return render(request, "page/index.html",ctx)

def index212(request):
    service = Kafedra.objects.all()
    ctx = {
        "services": service
    }

    if request.user.ut == 1:
        ctx.update(notifis())

    # return render(request, "page/index.html",ctx)




def search_results(request):
    query = request.GET.get('q')
    results =Cited_by.objects.filter(name=query)  # Misolcha, o'zgartiring
    if results is None:
        context = {
            'roots': results,
            'query': query,

        }
        return render(request, 'page/pr.html', context)
    else:
        return render(request, 'page/pr.html',{'error':query})