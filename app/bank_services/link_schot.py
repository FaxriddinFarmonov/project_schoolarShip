from decimal import Decimal
from django.shortcuts import render, redirect
from django.urls import reverse
from app.forms import LinkSchotForm
from app.models.create_schot import LinkSchot
import requests
import xml.etree.ElementTree as ET

def contract_update_view(request):
    form = LinkSchotForm()

    if request.method == 'POST':
        form = LinkSchotForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print("✅ Form maʼlumotlari:", cd)

            contract_rid = cd.get('Rid')
            client_rid = cd.get('ClientRid')
            type_rid = cd.get('TypeRid')
            branch_code = cd.get('BranchCode')

            xml_data = f"""<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <tw:Tran xmlns:tw="http://schemas.tranzaxis.com/tran.wsdl"
             xmlns:tran="http://schemas.tranzaxis.com/tran.xsd">
      <tran:Request xmlns="http://schemas.tranzaxis.com/contracts-admin.xsd"
                    xmlns:tran="http://schemas.tranzaxis.com/tran.xsd"
                    InitiatorRid="TURON"
                    LifePhase="Single"
                    Kind="ModifyContract">
        <tran:Specific>
          <tran:Admin ObjectMustExist="false">
            <tran:Contract Rid="{contract_rid}">
              <BranchCode>{branch_code}</BranchCode>
              <TypeRid>{type_rid}</TypeRid>
              <ClientRid>{client_rid}</ClientRid>
            </tran:Contract>
          </tran:Admin>
        </tran:Specific>
      </tran:Request>
    </tw:Tran>
  </soap:Body>
</soap:Envelope>"""

            headers = {"Content-Type": "text/xml; charset=utf-8"}

            try:
                response = requests.post("http://172.31.77.12:10011", data=xml_data.encode("utf-8"), headers=headers)
                print("🔵 SOAP Response:\n", response.text)

                tree = ET.fromstring(response.text)
                ns = {
                    'soap': "http://schemas.xmlsoap.org/soap/envelope/",
                    'tran': "http://schemas.tranzaxis.com/tran.xsd",
                    '': "http://schemas.tranzaxis.com/contracts-admin.xsd"
                }

                body = tree.find(".//soap:Body", ns)
                fault = body.find(".//soap:Fault", ns)

                if fault is not None:
                    result = {"Xatolik": fault.findtext("faultstring", default="Nomaʼlum xato")}
                else:
                    response_tag = body.find(".//tran:Response", ns)
                    contract_tag = body.find(".//tran:Contract", ns)
                    account_tag = contract_tag.find(".//Account", ns) if contract_tag is not None else None

                    branch_name = contract_tag.findtext(".//BranchName", default="", namespaces=ns)
                    branch_code = contract_tag.findtext(".//BranchCode", default="", namespaces=ns)
                    inst_name = contract_tag.attrib.get("InstName", "")
                    contract_rid_resp = contract_tag.attrib.get("Rid", "")
                    client_id = contract_tag.findtext(".//ClientId", default="", namespaces=ns)
                    currency = account_tag.attrib.get("Ccy", "") if account_tag is not None else ""
                    balance = account_tag.findtext(".//Balance", default="0", namespaces=ns)
                    credit_hold = account_tag.findtext(".//CreditHold", default="0", namespaces=ns)
                    debit_hold = account_tag.findtext(".//DebitHold", default="0", namespaces=ns)
                    plan_item_guid = account_tag.attrib.get("PlanItemGuid", "") if account_tag is not None else ""

                    LinkSchot.objects.create(
                        customer=cd['customer'],
                        TypeRid=cd['TypeRid'],
                        ClientRid=cd['ClientRid'],
                        Rid=cd['Rid'],
                        BranchName=branch_name,
                        BranchCode=branch_code,
                        InstName=inst_name,
                        ContractRid=contract_rid_resp,
                        ClientId=client_id,
                        Currency=currency,
                        Balance=Decimal(balance),
                        CreditHold=Decimal(credit_hold),
                        DebitHold=Decimal(debit_hold),
                        PlanItemGuid=plan_item_guid
                    )

                    result = {
                        "Success": "✅ Kontrakt maʼlumotlari muvaffaqiyatli yuborildi va bazaga saqlandi.",
                        "ApprovalCode": response_tag.get("ApprovalCode") if response_tag is not None else "yo‘q"
                    }

                request.session["result"] = result
                request.session["soap_raw"] = response.text
                request.session["show_form"] = False

            except Exception as e:
                request.session["result"] = {"Xato": str(e)}
                request.session["soap_raw"] = ""
                request.session["show_form"] = False

            return redirect(reverse("get_schot"))

    result = request.session.pop("result", None)
    soap_raw = request.session.pop("soap_raw", None)
    show_form = request.session.pop("show_form", True)

    return render(request, "page/link_schot.html", {
        "form": form,
        "result": result,
        "soap_raw": soap_raw,
        "show_form": show_form,
        "pos": "form"
    })
