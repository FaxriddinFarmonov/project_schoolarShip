from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.conf import   settings
from app.models import User


def list_members(request,type=None):
    kwargs = {"ut":type} if type else {}


    pagination = User.objects.filter(kwargs).order_by('-pk')
    paginator = Paginator(pagination, settings.PAGINATE_BY)
    page_number = requests.GET.get("page", 1)
    paginated = paginator.get_page(page_number)


