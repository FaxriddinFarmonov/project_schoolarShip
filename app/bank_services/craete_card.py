import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.urls import reverse
from app.services.forms.create_card import CardModifyForm
from app.models.create_card import CardModify

def modify_card_view(request):
    form = CardModifyForm(request.POST or None)
    print("------------------")

    if request.method == "POST" and form.is_valid():
        print("------------------")
        obj = form.save(commit=False)

        # SOAP XML
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
          <tran:Admin>
            <tran:Token>
              <Card>
                <ExtRid>{obj.extrid}</ExtRid>
                <ContractRid>{obj.extrid}</ContractRid>
                <ProductRid>VisaNEWBIN</ProductRid>
                <CreateContractTypeRid>42403293</CreateContractTypeRid>
                <CreateContractClientRid>{obj.extrid}</CreateContractClientRid>
                <CreateContractOutLinks>
                  <Link Kind="Access" Contract2Rid="{obj.contract2rid}">
                    <con:Status>A</con:Status>
                  </Link>
                </CreateContractOutLinks>
                <CurBranchCode>{obj.cur_branch_code}</CurBranchCode>
                <DeliveryBranchCode>{obj.cur_branch_code}</DeliveryBranchCode>
                <LifePhaseRid>New</LifePhaseRid>
              </Card>
            </tran:Token>
          </tran:Admin>
        </tran:Specific>
      </tran:Request>
    </tw:Tran>
  </soap:Body>
</soap:Envelope>"""

        headers = {"Content-Type": "text/xml; charset=utf-8"}

        try:
            response = requests.post("http://172.31.77.12:10011", data=xml_data.encode("utf-8"), headers=headers, timeout=30)

            # Javobni parse qilish
            tree = ET.fromstring(response.text)
            ns = {
                "tran": "http://schemas.tranzaxis.com/tran.xsd",
                "tok": "http://schemas.tranzaxis.com/tokens-admin.xsd"
            }

            response_tag = tree.find(".//tran:Response", ns)
            if response_tag is not None:
                obj.response_id = response_tag.attrib.get("Id", "")
                obj.result = response_tag.attrib.get("Result", "")
                obj.approval_code = response_tag.attrib.get("ApprovalCode", "")

                cardvsdc = tree.find(".//tok:CardVsdc", ns)
                if cardvsdc is not None:
                    obj.cardvsdc_id = cardvsdc.attrib.get("Id", "")

            obj.save()
            print(obj.result,"--------------------------------")

            request.session["result"] = {
                "ResponseId": obj.response_id,
                "Result": obj.result,
                "ApprovalCode": obj.approval_code,
                "CardVsdcId": obj.cardvsdc_id
            }
        except Exception as e:
            request.session["result"] = {"Xatolik": str(e)}

        return redirect(reverse("get_create_card"))

    result = request.session.pop("result", None)
    return render(request, "page/create_card.html", {
        "form": form,
         "result": result,
        "pos": "form"
    })

