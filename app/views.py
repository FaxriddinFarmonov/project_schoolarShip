from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.forms import CardPanForm
from app.models import Kafedra
# from app.models.doctor import Cited_by
from app.services.derector import notifis


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



#
# def search_results(request):
#     query = request.GET.get('q')
#     results =Cited_by.objects.filter(name=query)  # Misolcha, o'zgartiring
#     print(results is not None)
#     if results :
#         context = {
#             'roots': results,
#             'query': query,
#
#         }
#         return render(request, 'page/pr.html', context)
#     else:
#         return render(request, 'page/search.html',{'error':query})



# views.py
import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from .forms import CardPanForm

# views.py
import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from app.forms import CardPanForm

import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from .forms import CardPanForm
#
# def get_balance_view(request):
#     result = None
#     form = CardPanForm()
#
#     if request.method == "POST":
#         form = CardPanForm(request.POST)
#         if form.is_valid():
#             card_pan = form.cleaned_data["card_pan"]
#
#             xml_data = f"""
#             <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
#                 xmlns:tran="http://schemas.tranzaxis.com/tran.xsd"
#                 xmlns:tranwsdl="http://schemas.tranzaxis.com/tran.wsdl">
#                 <soapenv:Header/>
#                 <soapenv:Body>
#                     <tranwsdl:Tran>
#                         <tran:Request InitiatorRid="TestBank" LifePhase="Single" Kind="GetCardInfo" ProcessorInstName="Test">
#                             <tran:Specific>
#                                 <tran:Card>
#                                     <tran:PAN>{card_pan}</tran:PAN>
#                                 </tran:Card>
#                             </tran:Specific>
#                         </tran:Request>
#                     </tranwsdl:Tran>
#                 </soapenv:Body>
#             </soapenv:Envelope>
#             """
#
#             headers = {"Content-Type": "text/xml; charset=utf-8"}
#
#             try:
#                 response = requests.post("http://172.31.77.12:10011", data=xml_data.encode("utf-8"), headers=headers)
#
#                 print("========== SOAP JAVOBI ==========")
#                 print(response.text)
#                 print("==================================")
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
#             except Exception as e:
#                 result = {"Xatolik": str(e)}
#
#     return render(request, "page/scopus.html", {"form": form, "result": result,'pos' : 'form'})



import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from .forms import CardPanForm
#
# def get_balance_view(request):
#     result = None
#     form = CardPanForm()
#
#     if request.method == "POST":
#         form = CardPanForm(request.POST)
#         if form.is_valid():
#             card_pan = form.cleaned_data["card_pan"]
#
#             # Siz yuborgan yangi SOAP format asosida
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
#             headers = {
#                 "Content-Type": "text/xml;charset=UTF-8"
#             }
#
#             try:
#                 response = requests.post("http://172.31.77.12:10011", data=xml_data.encode("utf-8"), headers=headers)
#
#                 # Terminalda ko‘rsatish
#                 print("========== SOAP JAVOBI ==========")
#                 print(response.text)
#                 print("==================================")
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
#             except Exception as e:
#                 result = {"Xatolik": str(e)}
#
#     return render(request, "page/scopus.html", {"form": form, "result": result, "pos": "form"})


from django.shortcuts import render, redirect
from django.urls import reverse  # kerak bo'ladi


# def get_balance_view(request):
#     form = CardPanForm()
#
#     if request.method == "POST":
#         form = CardPanForm(request.POST)
#         if form.is_valid():
#             card_pan = form.cleaned_data["card_pan"]
#
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
#                 # Session orqali uzatamiz
#                 request.session["result"] = result
#                 request.session["soap_raw"] = response.text
#
#                 return redirect(reverse("get-balance"))  # URL name ni yozing
#
#             except Exception as e:
#                 request.session["result"] = {"Xatolik": str(e)}
#                 return redirect(reverse("get_fak"))
#
#     # GET bo‘lsa
#     result = request.session.pop("result", None)
#     soap_raw = request.session.pop("soap_raw", None)
#
#     return render(request, "page/scopus.html", {
#         "form": form,
#         "result": result,
#         "soap_raw": soap_raw,
#         "pos": "form"
#     })


from django.shortcuts import render, redirect
from django.urls import reverse
import xml.etree.ElementTree as ET
import requests
from .forms import CardPanForm
#
# def get_balance_view(request):
#     form = CardPanForm()
#
#     if request.method == "POST":
#         form = CardPanForm(request.POST)
#         if form.is_valid():
#             card_pan = form.cleaned_data["card_pan"]
#
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
#                 request.session["result"] = result
#                 request.session["soap_raw"] = response.text
#                 request.session["show_form"] = False  # faqat natija ko‘rsatish
#
#
#             except Exception as e:
#                 request.session["result"] = {"Xatolik": str(e)}
#                 request.session["show_form"] = False
#                 return redirect(reverse("get-balance"))
#
#     # GET bo‘lsa
#     result = request.session.pop("result", None)
#     soap_raw = request.session.pop("soap_raw", None)
#     show_form = request.session.pop("show_form", True)  # default: True
#
#     return render(request, "page/scopus.html", {
#         "form": form,
#         "result": result,
#         "soap_raw": soap_raw,
#         "pos": "form",
#         "show_form": show_form
#     })
#
#
#     return redirect(reverse("dashboard-auto-add"))

# import requests
# import xml.etree.ElementTree as ET
# from django.shortcuts import render, redirect
# from django.urls import reverse
# from .forms import CardPanForm
# from models.doctor import Get_Balance
#
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
#                 print("🔁 SOAP javobi:", result)
#
#                 request.session["result"] = result
#                 request.session["soap_raw"] = response.text
#                 request.session["show_form"] = False  # faqat natija chiqadi
#
#             except Exception as e:
#                 print("❌ SOAP xatolik:", e)
#                 request.session["result"] = {"Xatolik": str(e)}
#                 request.session["show_form"] = False
#
#             return redirect(reverse("get_fak"))  # POST dan keyin redirect (PRG pattern)
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
#         "pos": "form"  # form qismida ko‘rsatsin
#     })




from .models import Get_Balance  # modelni import qilishni unutmang

def get_balance_view(request):
    form = CardPanForm()

    if request.method == "POST":
        form = CardPanForm(request.POST)
        if form.is_valid():
            card_pan = form.cleaned_data["card_pan"]

            # SOAP XML tayyorlash
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
                    if numval or intval:
                        Get_Balance.objects.create(NumVal=numval, IntVal=intval)

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
