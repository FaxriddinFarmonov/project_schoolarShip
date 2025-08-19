import requests
from django.shortcuts import render, redirect
from app.models.limit_card import CardRestriction
import xml.etree.ElementTree as ET
from app.services.forms.limet_card import CardRestrictionForm



def send_card_restriction(request):
    if request.method == "POST":
        form = CardRestrictionForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            max_val = form.cleaned_data['max_value']   # ✅ to‘g‘rilandi
            currency = form.cleaned_data['currency']   # masalan: 860 (UZS)

            # SOAP so‘rov yuborish
            soap_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                              xmlns:tran="http://schemas.tranzaxis.com/tran.wsdl"
                              xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd"
                              xmlns:tok="http://schemas.tranzaxis.com/tokens-admin.xsd"
                              xmlns:res="http://schemas.tranzaxis.com/restricting-admin.xsd">
               <soapenv:Header/>
               <soapenv:Body>
                  <tran:Tran>
                     <tran1:Request InitiatorRid="TURON"
                                    LifePhase="Single"
                                    Kind="ModifyToken"
                                    ProcessorInstName="Test">
                        <tran1:Specific>
                           <tran1:Admin ObjectMustExist="true">
                              <tran1:Token>
                                 <tok:Card>
                                    <tok:ExtRid>{card_number}</tok:ExtRid>
                                    <tok:Restrictions Mode="Change">
                                       <tok:Restriction ClassGuid="aclHTJOJ5BIQLOBDCKAAALOMT5GDM">
                                          <res:Rid>EXTID_CARD_RESTRICTION</res:Rid>
                                          <res:MaxVal>{max_val}</res:MaxVal>
                                          <res:Ccy>{currency}</res:Ccy>
                                          <res:ResetTime>0</res:ResetTime>
                                          <res:ResetPeriodType>Day</res:ResetPeriodType>
                                          <res:InUse>true</res:InUse>
                                       </tok:Restriction>
                                    </tok:Restrictions>
                                 </tok:Card>
                              </tran1:Token>
                           </tran1:Admin>
                        </tran1:Specific>
                     </tran1:Request>
                  </tran:Tran>
               </soapenv:Body>
            </soapenv:Envelope>
            """

            headers = {"Content-Type": "text/xml; charset=utf-8"}
            response = requests.post("http://172.31.77.12:10011", data=soap_body, headers=headers)

            # XML javobni parse qilish
            tree = ET.fromstring(response.text)
            ns = {
                "tran": "http://schemas.tranzaxis.com/tran.xsd",
                "tok": "http://schemas.tranzaxis.com/tokens-admin.xsd",
            }

            result = tree.find(".//tran:Response", ns).attrib.get("Result")
            approval_code = tree.find(".//tran:Response", ns).attrib.get("ApprovalCode")
            card_id = tree.find(".//tok:CardVsdc", ns).attrib.get("Id") if tree.find(".//tok:CardVsdc", ns) is not None else None
            restriction_guid = tree.find(".//tok:Restriction", ns).attrib.get("Guid") if tree.find(".//tok:Restriction", ns) is not None else None

            # Maskalash
            def mask_card_number(num):
                return num[0:4] + "*" * (len(num) - 8) + num[-4:]

            # Statusni shart bilan aniqlash
            status_value = "Limited" if approval_code == "Approved" else ""

            # Modelga yozish
            CardRestriction.objects.create(
                card_number=mask_card_number(card_number),
                result=result,
                approval_code=approval_code,
                card_id=card_id,
                restriction_guid=restriction_guid,
                status=status_value
            )

            return redirect("get_limit_card")
    else:
        form = CardRestrictionForm()

    return render(request, "page/limit_card.html", {
        "form": form,
        "pos": "form"
    })
