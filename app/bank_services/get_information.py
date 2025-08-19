import requests
from django.shortcuts import render
from app.services.forms.get_card import CardRequestForm
from app.models.get_card import CardInfo
from xml.etree import ElementTree as ET
from django.shortcuts import render, redirect
from django.urls import reverse

SOAP_TEMPLATE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:tran="http://schemas.tranzaxis.com/tran.wsdl"
 xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd"
 xmlns:tok="http://schemas.tranzaxis.com/tokens-admin.xsd">
   <soapenv:Header/>
   <soapenv:Body>
      <tran:Tran>
         <tran1:Request InitiatorRid="TURON" LifePhase="Single" Kind="ReadToken" ProcessorInstName="Test">
            <tran1:Specific>
               <tran1:Admin ObjectMustExist="true">
                  <tran1:Token>
                     <tok:Card>
                        <tok:ExtRid>{card_ext_rid}</tok:ExtRid>
                     </tok:Card>
                  </tran1:Token>
               </tran1:Admin>
            </tran1:Specific>
         </tran1:Request>
      </tran:Tran>
   </soapenv:Body>
</soapenv:Envelope>
"""

def card_lookup_view(request):
    if request.method == "POST":
        form = CardRequestForm(request.POST)
        if form.is_valid():
            card_ext_rid = form.cleaned_data['card_ext_rid']
            soap_body = SOAP_TEMPLATE.format(card_ext_rid=card_ext_rid)

            headers = {"Content-Type": "text/xml; charset=utf-8"}
            url = "http://172.31.77.12:10011"

            response = requests.post(url, data=soap_body.encode('utf-8'), headers=headers, timeout=10)

            if response.status_code == 200:
                tree = ET.fromstring(response.text)

                ns = {
                    'tran': "http://schemas.tranzaxis.com/tran.xsd",
                    'tok': "http://schemas.tranzaxis.com/tokens-admin.xsd",
                    'res': "http://schemas.tranzaxis.com/restricting-admin.xsd"
                }

                card_vsdc = tree.find('.//tok:CardVsdc', ns)

                if card_vsdc is not None:
                    card_pan = card_vsdc.attrib.get("Pan", "")
                    masked_pan = f"{card_pan[:6]}******{card_pan[-4:]}" if len(card_pan) == 16 else "****MASK ERROR"

                    data = CardInfo.objects.create(
                        card_ext_rid=card_ext_rid,
                        card_id=card_vsdc.attrib.get("Id"),
                        pan=masked_pan,
                        result=tree.find('.//tran:Response', ns).attrib.get("Result"),
                        approval_code=tree.find('.//tran:Response', ns).attrib.get("ApprovalCode"),
                        contract_rid=card_vsdc.findtext('tok:ContractRid', namespaces=ns),
                        product_rid=card_vsdc.findtext('tok:ProductRid', namespaces=ns),
                        status=card_vsdc.findtext('tok:Status', namespaces=ns),
                        create_time=card_vsdc.findtext('tok:CreateTime', namespaces=ns),
                        activate_day=card_vsdc.findtext('tok:ActivateDay', namespaces=ns),
                        activate_username=card_vsdc.findtext('tok:ActivateUserName', namespaces=ns),
                        exp_time=card_vsdc.findtext('tok:ExpTime', namespaces=ns),
                        max_val=card_vsdc.findtext('.//tok:Restriction/res:MaxVal', namespaces=ns) or 0,
                        ccy=card_vsdc.findtext('.//tok:Restriction/res:Ccy', namespaces=ns) or '',
                        pvv=card_vsdc.findtext('tok:Pvv', namespaces=ns),
                        emboss_name=card_vsdc.findtext('tok:EmbossName', namespaces=ns),
                        track_name=card_vsdc.findtext('tok:TrackName', namespaces=ns),
                        print_name=card_vsdc.findtext('tok:PrintName', namespaces=ns),
                        total_amt_up_lmt=card_vsdc.findtext('tok:TotalAmtUpLmt', namespaces=ns) or 0,
                        total_amt_lw_lmt=card_vsdc.findtext('tok:TotalAmtLwLmt', namespaces=ns) or 0,
                        total_cnt_up_lmt=card_vsdc.findtext('tok:TotalCntUpLmt', namespaces=ns) or 0,
                        total_cnt_lw_lmt=card_vsdc.findtext('tok:TotalCntLwLmt', namespaces=ns) or 0,
                        invalid_cap_tries_cnt=card_vsdc.findtext('tok:InvalidCapTriesCnt', namespaces=ns) or 0,
                    )

                    return redirect(reverse("get_card_information"))

    else:
        form = CardRequestForm()
    return render(request, "page/get_card.html", {
        "form": form,
        "pos": "form"
                                                  })
