import xlwt
import os
import zipfile
from io import BytesIO
from django.http import HttpResponse
from app.models.get_card import CardInfo


def export_all_cardinfo_zip(request):
    """
    CardInfo dagi barcha yozuvlarni har birini alohida Excel qilib, ZIP qilib qaytaradi.
    card_ext_rid ustuni chiqarilmaydi.
    """
    # Model ustunlarini olish (card_ext_rid ni chiqaramiz)
    fields = [f.name for f in CardInfo._meta.fields if f.name != 'card_ext_rid']
    field_verbose = [CardInfo._meta.get_field(f).verbose_name or f for f in fields]

    output_zip_stream = BytesIO()

    with zipfile.ZipFile(output_zip_stream, 'w', zipfile.ZIP_DEFLATED) as out_zip:
        for obj in CardInfo.objects.all():
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('CardInfo')

            # Header
            header_style = xlwt.XFStyle()
            header_style.font.bold = True
            for col_num, col_name in enumerate(field_verbose):
                ws.write(0, col_num, col_name, header_style)

            # Data
            body_style = xlwt.XFStyle()
            for col_num, field_name in enumerate(fields):
                value = getattr(obj, field_name)
                ws.write(1, col_num, str(value) if value is not None else "", body_style)

            # Excel’ni memoryga yozamiz
            excel_stream = BytesIO()
            wb.save(excel_stream)
            excel_stream.seek(0)

            # ZIP ichiga qo‘shamiz
            filename = f"cardinfo_{obj.id}.xls"
            out_zip.writestr(filename, excel_stream.read())

    output_zip_stream.seek(0)
    response = HttpResponse(output_zip_stream, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=cardinfo_all.zip'
    return response
