
from django.contrib.auth.decorators import login_required

from app.models import Kafedra
from app.services.derector import notifis
import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.urls import reverse
from app.forms import CardActivationForm
from app.models import CardActivation
from django.shortcuts import render
from .forms import BalanceUpdateForm
import requests






# Create your views here.
@login_required(login_url='login')
def index(request):
    service = Kafedra.objects.all()
    ctx = {
        "services": service
    }
    if request.user.ut == 1:
        ctx.update(notifis())
    return render(request, "page/index.html",ctx)




def index212(request):
    service = Kafedra.objects.all()
    ctx = {
        "services": service
    }

    if request.user.ut == 1:
        ctx.update(notifis())

    return render(request, "page/index.html",ctx)






from app.models import Get_Balance  # modelni import qilishni unutmang
#
# def get_balance_view(request):
#     form = CardPanForm()
#
#     if request.method == "POST":
#         form = CardPanForm(request.POST)
#         if form.is_valid():
#             card_pan = form.cleaned_data["card_pan"]
#
#             # SOAP XML tayyorlash
#             xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
# <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
#                   xmlns:tran="http://schemas.tranzaxis.com/tran.wsdl"
#                   xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd"
#                   xmlns:common="http://schemas.tranzaxis.com/tran-common.xsd">
#    <soapenv:Header/>
#    <soapenv:Body>
#       <tran:Tran>
#          <tran1:Request xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd"
#                         xmlns:common="http://schemas.tranzaxis.com/tran-common.xsd"
#                         InitiatorRid="TURON"
#                         LifePhase="Single"
#                         Kind="GetContractInfo">
#             <tran1:Parties>
#                <tran1:Cust AuthChecked="true">
#                   <tran1:Token Kind="Card">
#                      <common:Card Pan="{card_pan}"/>
#                   </tran1:Token>
#                </tran1:Cust>
#             </tran1:Parties>
#             <tran1:Specific>
#                <tran1:CustInfo Kinds="ContractAvailBalance ContractCcy"/>
#             </tran1:Specific>
#          </tran1:Request>
#       </tran:Tran>
#    </soapenv:Body>
# </soapenv:Envelope>"""
#
#             headers = {"Content-Type": "text/xml;charset=UTF-8"}
#
#             try:
#                 response = requests.post("http://172.31.77.12:10011", data=xml_data.encode("utf-8"), headers=headers)
#
#                 tree = ET.fromstring(response.text)
#                 body = tree.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")
#
#                 fault = body.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Fault")
#                 if fault is not None:
#                     result = {"Xato": fault.findtext("faultstring", default="Nomaʼlum xatolik")}
#                 else:
#                     result = {}
#                     for elem in body.iter():
#                         tag = elem.tag.split("}")[-1]
#                         if elem.text and elem.text.strip():
#                             result[tag] = elem.text.strip()
#
#                     print("🔁 SOAP javobi:", result)
#
#                     # 🔽 MODELGA SAQLAYMIZ
#                     numval = result.get("NumVal")
#                     intval = result.get("IntVal")
#                     if numval or intval:
#                         Get_Balance.objects.create(NumVal=numval, IntVal=intval)
#
#                 request.session["result"] = result
#                 request.session["soap_raw"] = response.text
#                 request.session["show_form"] = False
#
#             except Exception as e:
#                 print("❌ SOAP xatolik:", e)
#                 request.session["result"] = {"Xatolik": str(e)}
#                 request.session["show_form"] = False
#
#             return redirect(reverse("get_fak"))
#
#     # GET
#     result = request.session.pop("result", None)
#     soap_raw = request.session.pop("soap_raw", None)
#     show_form = request.session.pop("show_form", True)
#
#     return render(request, "page/scopus.html", {
#         "form": form,
#         "result": result,
#         "soap_raw": soap_raw,
#         "show_form": show_form,
#         "pos": "form"
#     })












from app.models import BlockCard  # model import
import re  # panni mask qilish uchun

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

            # ✅ SHART: oldin "Blocked" bo'lganmi?
            # if BlockCard.objects.filter(card_number=masked_pan, status="Blocked").exists():
            #     request.session["result"] = {"Xatolik": "Bu karta allaqachon bloklangan."}
            #     request.session["soap_raw"] = ""
            #     request.session["show_form"] = False
            #     return redirect(reverse("card_block"))

            # SOAP XML tayyorlash
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
              <Card>
                <ExtRid>{card_pan}</ExtRid>
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
                    result = {"Xato": fault.findtext("faultstring", default="Nomaʼlum xatolik")}
                    response_message = result["Xato"]
                else:
                    result = {}
                    for elem in body.iter():
                        tag = elem.tag.split("}")[-1]
                        if elem.text and elem.text.strip():
                            result[tag] = elem.text.strip()
                    response_message = "Successful ✅"

                print("🔁 SOAP javobi:", result)

                # 🔽 Modelga yozish
                BlockCard.objects.create(
                    card_number=masked_pan,
                    status="Blocked",
                    response_message=response_message
                )

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










from .forms import CardPanForm
from .models import Get_Balance

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

                    # 🔽 MODELGA SAQLAYMIZ
                    numval = result.get("NumVal")
                    intval = result.get("IntVal")

                    # ✅ Karta raqamini yulduzcha qilish
                    masked_pan = f"{card_pan[:6]}******{card_pan[-4:]}" if len(card_pan) == 16 else "****MASK ERROR"

                    if numval or intval:
                        Get_Balance.objects.create(
                            card_number=masked_pan,
                            NumVal=numval,
                            IntVal=intval
                        )

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











def activate_card(request):
    form = CardActivationForm()

    if request.method == 'POST':
        form = CardActivationForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']

            # ❗ Oldin active qilinganmi, tekshiramiz
            # existing = CardActivation.objects.filter(ext_rid=card_number, status="Active").first()
            # if BlockCard.objects.filter(card_number=masked_pan, status="Blocked").exists():Active
            # if existing:
                # ❗ Sessionga xabar
                # request.session["result"] = {"Xatolik": "Bu karta allaqachon Active qilingan"}
                # request.session["soap_raw"] = ""
                # request.session["show_form"] = False
                # return redirect(reverse("active_card_status"))

            # 🧾 SOAP XML tayyorlash
            xml_data = f"""<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <tw:Tran xmlns:tw="http://schemas.tranzaxis.com/tran.wsdl"
             xmlns:tran="http://schemas.tranzaxis.com/tran.xsd">
      <tran:Request xmlns:card="http://schemas.tranzaxis.com/tokens-admin.xsd"
                    xmlns:tran="http://schemas.tranzaxis.com/tran.xsd"
                    xmlns:com="http://schemas.tranzaxis.com/common-types.xsd"
                    xmlns:ctrt="http://schemas.tranzaxis.com/contracts-admin.xsd"
                    InitiatorRid="TURON"
                    LifePhase="Single"
                    Kind="ModifyToken">
        <tran:Specific>
          <tran:Admin>
            <tran:Token>
              <card:Card>
                <card:Status>Active</card:Status>
                <card:ExtRid>{card_number}</card:ExtRid>
              </card:Card>
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
                    result = {"Xato": fault.findtext("faultstring", default="Nomaʼlum xatolik")}
                else:
                    result = {}
                    for elem in body.iter():
                        tag = elem.tag.split("}")[-1]
                        if elem.text and elem.text.strip():
                            result[tag] = elem.text.strip()

                    # ✅ Masked card number saqlash
                    masked_card = f"{card_number[:6]}******{card_number[-4:]}" if len(card_number) >= 10 else "****MASK ERROR"
                    CardActivation.objects.create(ext_rid=card_number,masked_card_number=masked_card)

                # 🔄 Sessionga joylash
                request.session["result"] = result
                request.session["soap_raw"] = response.text
                request.session["show_form"] = False

            except Exception as e:
                print("❌ SOAP xatolik:", e)
                request.session["result"] = {"Xatolik": str(e)}
                request.session["show_form"] = False

            return redirect(reverse("active_card_status"))

    # GET
    result = request.session.pop("result", None)
    soap_raw = request.session.pop("soap_raw", None)
    show_form = request.session.pop("show_form", True)

    return render(request, "page/active_card.html", {
        "form": form,
        "result": result,
        "soap_raw": soap_raw,
        "show_form": show_form,
        "pos": "form"
    })





def balance_update_view(request):
    message = ""
    if request.method == 'POST':
        form = BalanceUpdateForm(request.POST)
        if form.is_valid():
            instance = form.save()

            xml_payload = f"""<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <tw:Tran xmlns:tw="http://schemas.tranzaxis.com/tran.wsdl"
             xmlns:tran="http://schemas.tranzaxis.com/tran.xsd">
      <tran:Request xmlns="http://schemas.tranzaxis.com/contracts-admin.xsd"
                    xmlns:tran="http://schemas.tranzaxis.com/tran.xsd"
                    LifePhase="Single"
                    InitiatorRid="TURON"
                    Kind="ModifyContract">
        <tran:Specific>
          <tran:Admin ObjectMustExist="true"
                      LastImpactedDay="2024-08-29T00:00:00"
                      LastImpactedTranId="0">
            <tran:Contract Rid="{instance.contract_rid}">
              <Accounts>
                <Account Ccy="{instance.currency}" Role="{instance.role}">
                  <Balance>{instance.balance}</Balance>
                </Account>
              </Accounts>
            </tran:Contract>
          </tran:Admin>
        </tran:Specific>
      </tran:Request>
    </tw:Tran>
  </soap:Body>
</soap:Envelope>
"""

            headers = {
                "Content-Type": "text/xml; charset=utf-8",
            }

            url = "https://your-soap-endpoint-url"  # <-- bu yerga to‘g‘ri URL qo‘ying
            response = requests.post(url, data=xml_payload.encode('utf-8'), headers=headers)

            message = f"Status: {response.status_code}\nResponse: {response.text}"

    else:
        form = BalanceUpdateForm()

    return render(request, 'page/payment.html', {'form': form, 'message': message})
