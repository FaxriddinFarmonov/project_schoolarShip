
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.urls import reverse
from app.forms import CardActivationForm
from app.models import CardActivation
from django.shortcuts import render
import requests
from app.forms import CardPanForm
from app.models import Get_Balance



def get_balance_view(request):
    form = CardPanForm()

    if request.method == "POST":
        form = CardPanForm(request.POST)
        if form.is_valid():
            card_pan = form.cleaned_data["card_pan"]

            # 🧾 SOAP XML tayyorlash
            xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:tran="http://schemas.tranzaxis.com/tran.wsdl" 
                  xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd"
                  xmlns:common="http://schemas.tranzaxis.com/tran-common.xsd">
   <soapenv:Header/>
   <soapenv:Body>
      <tran:Tran>    
         <tran1:Request xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd" 
                        xmlns:common="http://schemas.tranzaxis.com/tran-common.xsd" 
                        InitiatorRid="TURON" 
                        LifePhase="Single" 
                        Kind="GetContractInfo">
            <tran1:Parties>
               <tran1:Cust AuthChecked="true">
                  <tran1:Token Kind="Card">
                     <common:Card Pan="{card_pan}"/>
                  </tran1:Token>
               </tran1:Cust>
            </tran1:Parties>
            <tran1:Specific>
               <tran1:CustInfo Kinds="ContractAvailBalance ContractCcy"/>
            </tran1:Specific>
         </tran1:Request>   
      </tran:Tran>
   </soapenv:Body>
</soapenv:Envelope>"""

            headers = {"Content-Type": "text/xml;charset=UTF-8"}

            try:
                response = requests.post("http://172.31.77.12:10011", data=xml_data.encode("utf-8"), headers=headers)

                tree = ET.fromstring(response.text)
                body = tree.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")

                fault = body.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Fault")
                if fault is not None:
                    result = {"Xato": fault.findtext("faultstring", default="Nomaʼlum xatolik")}
                else:
                    result = {}
                    for elem in body.iter():
                        tag = elem.tag.split("}")[-1]
                        if elem.text and elem.text.strip():
                            result[tag] = elem.text.strip()

                    print("🔁 SOAP javobi:", result)

                    # ✅ Mask qilamiz
                    masked_pan = f"{card_pan[:6]}******{card_pan[-4:]}" if len(card_pan) == 16 else "****MASK ERROR"

                    # 🔍 tran:Response atributlari
                    ns = {
                        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
                        'tran': "http://schemas.tranzaxis.com/tran.xsd"
                    }
                    response_tag = body.find(".//tran:Response", ns)

                    response_id = response_tag.attrib.get("Id", "") if response_tag is not None else ""
                    approval_code = response_tag.attrib.get("ApprovalCode", "") if response_tag is not None else ""
                    result_status = response_tag.attrib.get("Result", "") if response_tag is not None else ""

                    # 🔽 Bazaga saqlaymiz
                    numval = result.get("NumVal")
                    intval = result.get("IntVal")

                    if numval or intval:
                        Get_Balance.objects.create(
                            card_number=masked_pan,
                            NumVal=numval,
                            IntVal=intval,
                            response_id=response_id,
                            approval_code=approval_code,
                            result=result_status
                        )

                # Sessionga saqlaymiz
                request.session["result"] = result
                request.session["soap_raw"] = response.text
                request.session["show_form"] = False

            except Exception as e:
                print("❌ SOAP xatolik:", e)
                request.session["result"] = {"Xatolik": str(e)}
                request.session["show_form"] = False

            return redirect(reverse("get_fak"))

    # GET
    result = request.session.pop("result", None)
    soap_raw = request.session.pop("soap_raw", None)
    show_form = request.session.pop("show_form", True)

    return render(request, "page/scopus.html", {
        "form": form,
        "result": result,
        "soap_raw": soap_raw,
        "show_form": show_form,
        "pos": "form"
    })
