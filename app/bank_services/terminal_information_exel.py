import openpyxl
from django.http import HttpResponse
from app.models import TerminalInfo


def export_terminalinfo_to_excel(request):
    # Excel workbook yaratamiz
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Terminal Info"

    # Sarlavhalar (result qo‘shilmagan!)
    headers = [
        "Terminal Name",
        "Terminal ID",
        "Terminal Inst ID",
        "Terminal Class Guid",
        "Terminal Class Title",
        "Terminal Status",
        "Terminal Dflt Ccy",
        "Terminal Accept Cash",
        "Terminal Address",
        "Created At",
    ]
    sheet.append(headers)

    # Barcha obyektlarni olib chiqamiz
    terminals = TerminalInfo.objects.all()

    for terminal in terminals:
        sheet.append([
            terminal.terminal_name,
            terminal.terminal_id,
            terminal.terminal_inst_id,
            terminal.terminal_class_guid,
            terminal.terminal_class_title,
            terminal.terminal_status,
            terminal.terminal_dflt_ccy,
            "Yes" if terminal.terminal_accept_cash else "No",  # Boolean uchun
            terminal.terminal_address,
            terminal.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    # Javob sifatida Excel qaytaramiz
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename=terminal_info.xlsx'

    workbook.save(response)
    return response
