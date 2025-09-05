import requests
import xml.etree.ElementTree as ET
from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models.read_terminal import TerminalRead
from app.BankSerializer.get_one_terminalSer import TerminalReadSerializer

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
    return elem.tag.rsplit("}", 1)[-1] if "}" in elem.tag else elem.tag


def _child_text(parent, local_name, default=""):
    for ch in list(parent):
        if _tag_name(ch) == local_name:
            return (ch.text or "").strip()
    return default


def _child_elem(parent, local_name):
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


class TerminalReadAPIView(APIView):
    def post(self, request):
        serializer = TerminalReadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        terminal_name = serializer.validated_data["terminal_name"]

        url = "http://172.31.77.12:10011"
        headers = {"Content-Type": "text/xml; charset=utf-8"}
        payload = SOAP_TEMPLATE.format(terminal_name=terminal_name)

        try:
            resp = requests.post(url, data=payload.encode("utf-8"), headers=headers, timeout=20)
        except requests.RequestException as e:
            return Response({"error": f"UZELGA ULANISHDA XATOLIK: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if resp.status_code != 200:
            return Response({"error": f"Server {resp.status_code} qaytardi"}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            tree = ET.fromstring(resp.text)
        except ET.ParseError as e:
            return Response({"error": f"XML parse xatosi: {e}", "raw_xml": resp.text}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Terminal elementini topish
        terminal_elem = None
        for el in tree.iter():
            if _tag_name(el) == "Terminal" and ("Id" in el.attrib or "Name" in el.attrib):
                terminal_elem = el
                break

        if not terminal_elem:
            return Response({"error": "Javobda Terminal elementi topilmadi.", "raw_xml": resp.text}, status=status.HTTP_404_NOT_FOUND)

        # Ma’lumotlarni yig‘ish
        addr_elem = _child_elem(terminal_elem, "Address")
        address = addr_elem.attrib if addr_elem is not None else None

        branch_elem = _child_elem(terminal_elem, "Branch")
        branch_id = _to_int(branch_elem.attrib.get("Id")) if branch_elem is not None else None
        branch_rid = branch_elem.attrib.get("Rid", "") if branch_elem is not None else ""
        branch_code = branch_elem.attrib.get("Code", "") if branch_elem is not None else ""

        owner_rid = ""
        for ch in list(terminal_elem):
            if "Rid" in getattr(ch, "attrib", {}):
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
            "host_password": _child_text(terminal_elem, "HostPassword", ""),
            "issuer_cards": _to_bool(_child_text(terminal_elem, "IssuerCards", "false")),
            "term_enhanced_password": _child_text(terminal_elem, "TermEnhancedPassword", ""),
        }

        # DB ga saqlash
        obj, _created = TerminalRead.objects.update_or_create(
            terminal_id=current_data["terminal_id"],
            defaults=current_data
        )

        return Response({"data": current_data, "saved": True, "raw_xml": resp.text}, status=status.HTTP_200_OK)
