from app.models import BlockCard  # model import

import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.urls import reverse
from app.forms import CardActivationForm, CardPanForm
from app.models import CardActivation
from django.shortcuts import render
import requests


def mask_card_number(pan):
    if len(pan) >= 10:
        return pan[:6] + '*' * (len(pan) - 10) + pan[-4:]
    return pan  # agar pan qisqa bo‘lsa, o‘zgarmaydi

def block_card_view(request):
    form = CardPanForm()

    if request.method == "POST":
        form = CardPanForm(request.POST)
        if form.is_valid():
            card_pan = form.cleaned_data["card_pan"]
            masked_pan = mask_card_number(card_pan)  # kartani mask qilish

            xml_data = f"""<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <tw:Tran xmlns:tw="http://schemas.tranzaxis.com/tran.wsdl"
             xmlns:tran="http://schemas.tranzaxis.com/tran.xsd">
      <tran:Request xmlns="http://schemas.tranzaxis.com/tokens-admin.xsd"
                    xmlns:tran="http://schemas.tranzaxis.com/tran.xsd"
                    xmlns:com="http://schemas.tranzaxis.com/common-types.xsd"
                    xmlns:con="http://schemas.tranzaxis.com/contracts-admin.xsd"
                    InitiatorRid="TURON"
                    LifePhase="Single"
                    Kind="ModifyToken">
        <tran:Specific>
          <tran:Admin ObjectMustExist="true">
            <tran:Token>
              <Card Pan="{card_pan}" FindByPan="true">
                <Status>Blocked</Status>
              </Card>
            </tran:Token>
          </tran:Admin>
        </tran:Specific>
      </tran:Request>
    </tw:Tran>
  </soap:Body>
</soap:Envelope>"""

            headers = {"Content-Type": "text/xml;charset=UTF-8"}

            try:
                response = requests.post("http://172.31.77.12:10011", data=xml_data.encode("utf-8"), headers=headers)

                tree = ET.fromstring(response.text)
                body = tree.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")

                fault = body.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Fault")
                if fault is not None:
                    response_message = fault.findtext("faultstring", default="Nomaʼlum xatolik")
                    result = {"Xato": response_message}

                    # ❌ Xatolik holati bazaga yoziladi
                    BlockCard.objects.create(
                        card_number=masked_pan,
                        status="Xatolik",
                        response_message=response_message
                    )
                else:
                    result = {}

                    # 🧩 Namespaces
                    ns = {
                        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
                        'tran': "http://schemas.tranzaxis.com/tran.xsd",
                        'tok': "http://schemas.tranzaxis.com/tokens-admin.xsd"
                    }

                    response_tag = body.find(".//tran:Response", ns)
                    token_tag = body.find(".//tok:CardVsdc", ns)

                    # 🔽 SOAP dan kerakli maydonlarni ajratamiz
                    response_id = response_tag.attrib.get("Id", "") if response_tag is not None else ""
                    approval_code = response_tag.attrib.get("ApprovalCode", "") if response_tag is not None else ""
                    result_status = response_tag.attrib.get("Result", "") if response_tag is not None else ""
                    card_id = token_tag.attrib.get("Id", "") if token_tag is not None else ""
                    response_message = "Bloklandi ✅"

                    # ✅ Bazaga saqlash
                    BlockCard.objects.create(
                        card_number=masked_pan,
                        status="Blocked",
                        response_message=response_message,
                        response_id=response_id,
                        approval_code=approval_code,
                        card_id=card_id,
                        result=result_status
                    )

                    # SOAP dan matnlar
                    for elem in body.iter():
                        tag = elem.tag.split("}")[-1]
                        if elem.text and elem.text.strip():
                            result[tag] = elem.text.strip()

                # Sessionga saqlash
                request.session["result"] = result
                request.session["soap_raw"] = response.text
                request.session["show_form"] = False

            except Exception as e:
                print("❌ SOAP xatolik:", e)
                result = {"Xatolik": str(e)}

                BlockCard.objects.create(
                    card_number=masked_pan,
                    status="Xatolik",
                    response_message=str(e)
                )

                request.session["result"] = result
                request.session["show_form"] = False

            return redirect(reverse("card_block"))

    # GET
    result = request.session.pop("result", None)
    soap_raw = request.session.pop("soap_raw", None)
    show_form = request.session.pop("show_form", True)

    return render(request, "page/block_card.html", {
        "form": form,
        "result": result,
        "soap_raw": soap_raw,
        "show_form": show_form,
        "pos": "form"
    })
