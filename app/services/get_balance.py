import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
#
# from app.forms import Teacher_scopusForm
#
#
# def get_balance_view(request):
#     result = None
#
#     if request.method == "POST":
#         form = Teacher_scopusForm(request.POST)
#         if form.is_valid():
#             pan = form.cleaned_data["card_pan"]
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
#                         InitiatorRid="SCHOLARSHIP"
#                         LifePhase="Single"
#                         Kind="GetCustomerInfo">
#             <tran1:Parties>
#                <tran1:Cust AuthChecked="true">
#                   <tran1:Token Kind="Card">
#                      <common:Card Pan="{pan}"/>
#                   </tran1:Token>
#                </tran1:Cust>
#             </tran1:Parties>
#             <tran1:Specific>
#                <tran1:CustInfo Kinds="Balance"/>
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
#                 response = requests.post(
#                     "http://172.31.77.12:10011",
#                     data=xml_data.encode("utf-8"),
#                     headers=headers
#                 )
#
#                 tree = ET.fromstring(response.text)
#                 body = tree.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")
#
#                 fault = body.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Fault")
#                 if fault is not None:
#                     result = {"error": "SOAP error"}
#                 else:
#                     result = {}
#                     for elem in body.iter():
#                         tag = elem.tag.split("}")[-1]
#                         if elem.text and elem.text.strip():
#                             result[tag] = elem.text.strip()
#
#             except Exception as e:
#                 result = {"error": str(e)}
#
#     else:
#         form = Teacher_scopusForm()
#
#     return render(request, "page/scopus.html", {"form": form, "result": result})
