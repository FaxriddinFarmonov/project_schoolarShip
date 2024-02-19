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


# def export_data_to_excel(request, key):
#     # Ma'lumotlarni olish
#     queryset = Graph.objects.filter(teacher_info__name=key)
#
#     # QuerySet dan DataFrame yaratish
#     data = list(queryset.values())
#     df = pd.DataFrame(data)
#
#     # Excel faylga yozish
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = f'attachment; filename="{key}_data.xlsx"'
#     df.to_excel(response, index=False)

    # import csv
    # from django.http import HttpResponse
    #
    #
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    #
    # writer = csv.writer(response)
    # writer.writerow(['ID', 'Name', '           Toplam    ', '  yil ','        Nomi          ','       Link        ','iqtiqboli'])
    #
    # for obj in Graph.objects.filter(teacher_info__name=key):
    #     writer.writerow([ obj.name        , obj.publication, obj.year,obj.title,obj.links,obj.value])
    #
    # return response

    # return response



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

from django.http import HttpResponse
import xlwt




def export_data_to_excel(request, key):

    # from myapp.models import MyModel


        # Ma'lumotlarni olish
        queryset = Graph.objects.filter(teacher_info__name=key)

        # Excel faylni yaratish
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename={key}_doc.xls'

        # Workbook yaratish
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Malumotlar')

        # Ma'lumotlarni yozish
        row_num = 0
        columns = [

            (u"name", 6000),
            (u"publication", 18020),
            (u"year", 1400),
            (u"title", 26000),
            (u"links", 15000),
            (u"value", 2000),

        ]

        # Headerlarni yozish
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # Uzunliklarni o'zgartirish
            ws.col(col_num).width = columns[col_num][1]

        # Ma'lumotlarni yozish
        font_style = xlwt.XFStyle()
        for obj in queryset:
            row_num += 1
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, getattr(obj, columns[col_num][0]), font_style)

        # Faylni HttpResponse orqali yuborish
        wb.save(response)
        return response

