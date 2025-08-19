import requests
from xml.etree import ElementTree as ET
from django.shortcuts import render, redirect
from django.urls import reverse
from app.models import TerminalInfo

SOAP_TEMPLATE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:tran="http://schemas.tranzaxis.com/tran.wsdl"
 xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd">
   <soapenv:Header/>
   <soapenv:Body>
      <tran:Tran>
         <tran1:Request InitiatorRid="TURON"
                        ProcessorInstId="41"
                        OriginatorInstId="41"
                        Kind="GetTerminalInfo"
                        LifePhase="Single"
                        IsAdvice="false">
            <tran1:Parties>
               <tran1:Term Id="108" Rid="POS120"/>
            </tran1:Parties>
            <tran1:Specific>
               <tran1:CustInfo 
                   Kinds="TerminalId TerminalContractId TerminalInstId TerminalClassGuid TerminalClassTitle TerminalExtRid
                          TerminalName TerminalTitle TerminalStatus TerminalStatusTitle TerminalOwnerMcc TerminalDfltCcy TerminalAddress
                          TerminalAddressLatitude TerminalAddressLongitude TerminalDistance TerminalCassetteInfo TerminalStateConnected TerminalAcceptCash"
                   Language="en"/>
            </tran1:Specific>
         </tran1:Request>
      </tran:Tran>
   </soapenv:Body>
</soapenv:Envelope>
"""



def terminal_lookup_view(request):
    url = "http://172.31.77.12:10011"
    headers = {"Content-Type": "text/xml; charset=utf-8"}

    response = requests.post(url, data=SOAP_TEMPLATE.encode("utf-8"), headers=headers, timeout=15)

    if response.status_code == 200:
        tree = ET.fromstring(response.text)
        ns = {
            "tran": "http://schemas.tranzaxis.com/tran.xsd",
            "tran1": "http://schemas.tranzaxis.com/tran-common.xsd"
        }

        for item in tree.findall(".//tran1:Item", ns):
            current_data = {}

            for attr in item.findall("tran1:Attribute", ns):
                kind = attr.attrib.get("Kind")

                if kind == "TerminalId":
                    current_data["terminal_id"] = int(attr.findtext("tran1:IntVal", default="0", namespaces=ns))
                elif kind == "TerminalInstId":
                    current_data["terminal_inst_id"] = int(attr.findtext("tran1:IntVal", default="0", namespaces=ns))
                elif kind == "TerminalClassGuid":
                    current_data["terminal_class_guid"] = attr.findtext("tran1:StrVal", default="", namespaces=ns)
                elif kind == "TerminalClassTitle":
                    current_data["terminal_class_title"] = attr.findtext("tran1:StrVal", default="", namespaces=ns)
                elif kind == "TerminalName":
                    current_data["terminal_name"] = attr.findtext("tran1:StrVal", default="", namespaces=ns)
                elif kind == "TerminalStatus":
                    current_data["terminal_status"] = attr.findtext("tran1:StrVal", default="", namespaces=ns)
                elif kind == "TerminalDfltCcy":
                    current_data["terminal_dflt_ccy"] = int(attr.findtext("tran1:IntVal", default="0", namespaces=ns))
                elif kind == "TerminalAcceptCash":
                    bool_val = attr.findtext("tran1:BoolVal", default="false", namespaces=ns)
                    current_data["terminal_accept_cash"] = (bool_val.lower() == "true")
                elif kind == "TerminalAddress":   # ✅ yangi qo‘shildi
                    current_data["terminal_address"] = attr.findtext("tran1:StrVal", default="", namespaces=ns)

            if current_data.get("terminal_id"):  # faqat terminal_id bo‘lsa
                TerminalInfo.objects.update_or_create(
                    terminal_id=current_data["terminal_id"],
                    defaults=current_data
                )

        return redirect(reverse("get_terminal_information"))

    return render(request, "page/terminal_informations.html", {"pos": "form"})
