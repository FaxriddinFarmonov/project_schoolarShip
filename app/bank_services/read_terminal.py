import requests
from xml.etree import ElementTree as ET
from django.shortcuts import render,redirect,reverse
from django.utils.dateparse import parse_datetime
from app.models.read_terminal import TerminalRead
from app.services.forms.read_terminal import TerminalReadForm

SOAP_TEMPLATE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:tran="http://schemas.tranzaxis.com/tran.wsdl"
                  xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd">
   <soapenv:Header/>
   <soapenv:Body>
      <tran:Tran>
         <tran1:Request InitiatorRid="TURON"
                        LifePhase="Single"
                        Kind="ReadTerminal"
                        ProcessorInstName="Test">
            <tran1:Specific>
               <tran1:Admin ObjectMustExist="true">
                  <tran1:Terminal Name="{terminal_name}"/>
               </tran1:Admin>
            </tran1:Specific>
         </tran1:Request>
      </tran:Tran>
   </soapenv:Body>
</soapenv:Envelope>"""

def _tag_name(elem):
    """'{ns}Local' -> 'Local'"""
    return elem.tag.rsplit("}", 1)[-1] if "}" in elem.tag else elem.tag

def _child_text(parent, local_name, default=""):
    """Namespace-dan mustaqil bola element matnini qaytaradi."""
    for ch in list(parent):
        if _tag_name(ch) == local_name:
            return (ch.text or "").strip()
    return default

def _child_elem(parent, local_name):
    """Namespace-dan mustaqil bola elementni qaytaradi."""
    for ch in list(parent):
        if _tag_name(ch) == local_name:
            return ch
    return None

def _to_int(val, default=None):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

def _to_bool(val):
    return str(val).strip().lower() in {"1", "true", "yes"}

def read_terminal_view(request):
    data = None
    error = None

    if request.method == "POST":
        form = TerminalReadForm(request.POST)
        if form.is_valid():
            terminal_name = form.cleaned_data["terminal_name"].strip()

            url = "http://172.31.77.12:10011"
            headers = {"Content-Type": "text/xml; charset=utf-8"}
            payload = SOAP_TEMPLATE.format(terminal_name=terminal_name)

            try:
                resp = requests.post(url, data=payload.encode("utf-8"), headers=headers, timeout=20)
            except requests.RequestException as e:
                error = f"UZELGA ULANISHDA XATOLIK: {e}"
                return render(request, "page/read_terminal.html", {"form": form, "data": data, "error": error, "pos": "form"})

            if resp.status_code != 200:
                error = f"Server {resp.status_code} qaytardi"
                return render(request, "page/read_terminal.html", {"form": form, "data": data, "error": error, "pos": "form"})

            # XML parse (namespace-agnostic)
            try:
                tree = ET.fromstring(resp.text)
            except ET.ParseError as e:
                error = f"XML parse xatosi: {e}"
                return render(request, "page/read_terminal.html", {"form": form, "data": data, "error": error, "pos": "form"})

            # Terminal elementini topish (prefixdan mustaqil)
            terminal_elem = None
            for el in tree.iter():
                if _tag_name(el) == "Terminal" and ("Id" in el.attrib or "Name" in el.attrib):
                    terminal_elem = el
                    break

            if not terminal_elem:
                error = "Javobda Terminal elementi topilmadi."
                return render(request, "page/read_terminal.html", {"form": form, "data": data, "error": error, "pos": "form"})

            # Ma’lumotlarni yig‘ish
            addr_elem = _child_elem(terminal_elem, "Address")
            address = addr_elem.attrib if addr_elem is not None else None

            branch_elem = _child_elem(terminal_elem, "Branch")
            branch_id = _to_int(branch_elem.attrib.get("Id")) if branch_elem is not None else None
            branch_rid = branch_elem.attrib.get("Rid", "") if branch_elem is not None else ""
            branch_code = branch_elem.attrib.get("Code", "") if branch_elem is not None else ""

            # Ba’zi javoblarda Owner/Acquirer kabilar bo‘lishi mumkin – owner_rid uchun izlaymiz
            owner_rid = ""
            for ch in list(terminal_elem):
                if "Rid" in getattr(ch, "attrib", {}):
                    # Branchdan tashqari bo‘lsa, owner_rid deb olamiz
                    if ch is not branch_elem:
                        owner_rid = ch.attrib.get("Rid", "")
                        if owner_rid:
                            break

            current_data = {
                "terminal_id": _to_int(terminal_elem.attrib.get("Id")),
                "terminal_name": terminal_elem.attrib.get("Name", ""),

                "class_guid": _child_text(terminal_elem, "ClassGuid", ""),
                "inst_name": _child_text(terminal_elem, "InstName", ""),
                "status": _child_text(terminal_elem, "Status", ""),
                "title": _child_text(terminal_elem, "Title", ""),
                "notes": _child_text(terminal_elem, "Notes", "") or None,

                "create_time": parse_datetime(_child_text(terminal_elem, "CreateTime", "")),
                "create_day": parse_datetime(_child_text(terminal_elem, "CreateDay", "")),
                "activate_time": parse_datetime(_child_text(terminal_elem, "ActivateTime", "")),

                "default_ccy": _to_int(_child_text(terminal_elem, "DefaultCcy", None)),
                "default_language": _child_text(terminal_elem, "DefaultLanguage", ""),

                "address": address,

                "branch_id": branch_id,
                "branch_rid": branch_rid,
                "branch_code": branch_code,
                "owner_rid": owner_rid,

                "last_rq_time": parse_datetime(_child_text(terminal_elem, "LastRqTime", "")),
                "last_resp_time": parse_datetime(_child_text(terminal_elem, "LastRespTime", "")),
                "last_online_rrn": _child_text(terminal_elem, "LastOnlineRrn", ""),
                "mac_error_cnt": _to_int(_child_text(terminal_elem, "MacErrorCnt", "0"), 0),

                # POS bo‘limlari ham namespace-agnostic qidiriladi
                "host_password": _child_text(terminal_elem, "HostPassword", ""),
                "issuer_cards": _to_bool(_child_text(terminal_elem, "IssuerCards", "false")),
                "term_enhanced_password": _child_text(terminal_elem, "TermEnhancedPassword", ""),
            }

            # Majburiy maydonlar tekshiruvi
            if current_data["terminal_id"] is None:
                error = "Javobda Terminal Id yo‘q."
                return render(request, "page/read_terminal.html", {"form": form, "data": data, "error": error, "pos": "form"})

            # Saqlash / yangilash
            obj, _created = TerminalRead.objects.update_or_create(
                terminal_id=current_data["terminal_id"],
                defaults=current_data
            )
            data = obj
            return redirect(reverse("read_terminal_information"))
    else:
        form = TerminalReadForm()

    return render(request, "page/read_terminal.html", {
        "form": form,
        "data": data,
        "error": error,
        "pos": "form",
    })
