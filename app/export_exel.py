from django.shortcuts import render,redirect
from app.models import Graph
import pandas as pd
from django.http import JsonResponse




from django.http import HttpResponse
import xlwt


import pandas as pd
from app.models.doctor import Graph

# def export_data_to_excel():
#     # Ma'lumotlarni olish
#     queryset = Graph.objects.all()
#     # QuerySet dan DataFrame yaratish
#     df = pd.DataFrame(list(queryset.values()))
#     # Excel fayliga yozish
#     df.to_excel('ma\'lumotlar.xlsx', index=False)


# from excel_response import ExcelResponse
# from app.models.doctor import Graph
#
# def export_data_to_excel(request,key):
#     # Ma'lumotlarni olish
#     queryset = Graph.objects.filter(teacher_info__name=key)
#     # QuerySet dan Excel faylga yozish
#
#     return ExcelResponse(queryset)


import pandas as pd
from django.http import HttpResponse

from app.models import Graph


def export_data_to_excel(request, key):
    # Ma'lumotlarni olish
    queryset = Graph.objects.filter(teacher_info__name=key)

    # QuerySet dan DataFrame yaratish
    data = list(queryset.values())
    df = pd.DataFrame(data)

    # Excel faylga yozish
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{key}_data.xlsx"'
    df.to_excel(response, index=False)

    return response



def export_data_to_excel_fak(request, key):
    # Ma'lumotlarni olish
    queryset = Graph.objects.filter(teacher_info__kafedra__name=key)

    # QuerySet dan DataFrame yaratish
    data = list(queryset.values())
    df = pd.DataFrame(data)

    # Excel faylga yozish
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{key}_data.xlsx"'
    df.to_excel(response, index=False)

    return response
