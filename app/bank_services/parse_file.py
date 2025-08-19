import re
import os
import zipfile
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from app.models.upload_file import UploadedFile
import xlwt
from io import BytesIO


def process_cash_withdrawal(content):
    """
    Matndan CASH WITHDRAWAL va CASH WITHDRAWAL FAULT ma'lumotlarini Excel faylga yozadi.
    """
    # Normal va Fault bloklarni topamiz
    normal_blocks = re.findall(
        r"=+\s*CASH WITHDRAWAL\s*=+\r?\n(.*?)(?==+|$)",
        content,
        re.DOTALL | re.IGNORECASE
    )
    fault_blocks = re.findall(
        r"=+\s*CASH WITHDRAWAL FAULT\s*=+\r?\n(.*?)(?==+|$)",
        content,
        re.DOTALL | re.IGNORECASE
    )

    # Agar hech narsa topilmasa None qaytaramiz
    if not normal_blocks and not fault_blocks:
        return None

    output_stream = BytesIO()
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Cash Withdrawals')

    # Sarlavhalar
    columns = [
        (u'Timestamp', 5000),
        (u'PAN', 8000),
        (u'Amount', 4000),
        (u'Currency', 3000),
        (u'Solution', 10000),
    ]

    header_style = xlwt.XFStyle()
    header_style.font.bold = True
    for col_num, (col_name, col_width) in enumerate(columns):
        ws.write(0, col_num, col_name, header_style)
        ws.col(col_num).width = col_width

    row_num = 1
    body_style = xlwt.XFStyle()

    def write_blocks(blocks, is_fault=False):
        nonlocal row_num
        for block in blocks:
            try:
                lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
                if len(lines) < 4:
                    continue

                timestamp_str = lines[0].split(" - ")[0].strip()
                timestamp = datetime.strptime(timestamp_str, "%Y.%m.%d %H:%M:%S")

                pan = lines[1].replace("PAN:", "").strip()
                amount_line = lines[2].replace("AMOUNT:", "").strip()
                amount_value = re.sub(r"[^\d.]", "", amount_line)
                amount = float(amount_value) if amount_value else 0

                currency = "UZS"
                solution = lines[3].replace("SOLUTION:", "").strip()
                if is_fault:
                    solution += " FAULT"

                row_data = [
                    timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    pan,
                    amount,
                    currency,
                    solution,
                ]

                for col_num, value in enumerate(row_data):
                    ws.write(row_num, col_num, value, body_style)

                row_num += 1
            except Exception as e:
                print(f"Xatolik blokda: {block}\nXatolik: {e}")

    # Avval normal yozuvlar
    write_blocks(normal_blocks, is_fault=False)
    # Keyin fault yozuvlar
    write_blocks(fault_blocks, is_fault=True)

    wb.save(output_stream)
    output_stream.seek(0)
    return output_stream


def export_cashwithdrawal_from_zip(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
        zip_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.file.name)

        if not zipfile.is_zipfile(zip_path):
            return HttpResponse("Bu ZIP fayl emas", status=400)

        output_zip_stream = BytesIO()

        with zipfile.ZipFile(zip_path, 'r') as zf:
            with zipfile.ZipFile(output_zip_stream, 'w', zipfile.ZIP_DEFLATED) as out_zip:
                for name in zf.namelist():
                    if name.lower().endswith(('.txt', '.jrn')):
                        with zf.open(name) as f:
                            content = f.read().decode('utf-8-sig', errors='ignore')
                            excel_stream = process_cash_withdrawal(content)
                            if excel_stream:  # faqat bo‘sh bo‘lmasa yozamiz
                                out_zip.writestr(
                                    f"{os.path.splitext(os.path.basename(name))[0]}.xls",
                                    excel_stream.read()
                                )

        output_zip_stream.seek(0)
        response = HttpResponse(output_zip_stream, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename=cash_withdrawals_{file_id}.zip'
        return response

    except UploadedFile.DoesNotExist:
        return HttpResponse("Fayl topilmadi", status=404)
