from django.shortcuts import render,redirect
from app.models import Graph
import pandas as pd
from django.http import JsonResponse




from django.http import HttpResponse
import xlwt
#
# def export_to_excel(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="ma\'lumotlar.xls"'
#
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Ma\'lumotlar')  # Worksheet nomi
#
#     # Ma'lumotlar (misolcha, siz o'zingizning ma'lumotlar tizimingizga mos ma'lumotlar kerak)
#     malumotlar = [
#         ['Ism', 'Yosh', 'Manzil'],
#         ['John', 30, 'New York'],
#         ['Jane', 25, 'London'],
#         # Qolgan ma'lumotlar
#     ]
#
#     # Ma'lumotlarni yozish
#     for row_num, row_data in enumerate(malumotlar):
#         for col_num, cell_data in enumerate(row_data):
#             ws.write(row_num, col_num, cell_data)
#
#     wb.save(response)

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


