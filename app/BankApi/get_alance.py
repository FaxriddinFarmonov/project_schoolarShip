import requests
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models import Get_Balance
from app.BankSerializer.get_balanceSer import CardBalanceSerializer


SOAP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:tran="http://schemas.tranzaxis.com/tran.wsdl" 
                  xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd"
                  xmlns:common="http://schemas.tranzaxis.com/tran-common.xsd">
   <soapenv:Header/>
   <soapenv:Body>
      <tran:Tran>    
         <tran1:Request InitiatorRid="TURON" LifePhase="Single" Kind="GetContractInfo">
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


class CardBalanceAPIView(APIView):
    def post(self, request):
        serializer = CardBalanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        card_pan = serializer.validated_data["card_pan"]

        # SOAP body tayyorlash
        soap_body = SOAP_TEMPLATE.format(card_pan=card_pan)
        headers = {"Content-Type": "text/xml;charset=UTF-8"}
        url = "http://172.31.77.12:10011"

        try:
            response = requests.post(
                url, data=soap_body.encode("utf-8"), headers=headers, timeout=15
            )
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        raw_xml = response.text

        try:
            tree = ET.fromstring(raw_xml)
            body = tree.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")

            # SOAP fault check
            fault = body.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Fault")
            if fault is not None:
                parsed_data = {
                    "error": fault.findtext("faultstring", default="Nomaʼlum xatolik")
                }
                return Response(
                    {"parsed_json": parsed_data, "raw_xml": raw_xml},
                    status=status.HTTP_200_OK
                )

            # XML parsing
            result = {}
            for elem in body.iter():
                tag = elem.tag.split("}")[-1]
                if elem.text and elem.text.strip():
                    result[tag] = elem.text.strip()

            ns = {
                "soap": "http://schemas.xmlsoap.org/soap/envelope/",
                "tran": "http://schemas.tranzaxis.com/tran.xsd",
            }
            response_tag = body.find(".//tran:Response", ns)

            response_id = approval_code = result_status = ""
            if response_tag is not None:
                response_id = response_tag.attrib.get("Id", "")
                approval_code = response_tag.attrib.get("ApprovalCode", "")
                result_status = response_tag.attrib.get("Result", "")

            numval = result.get("NumVal")
            intval = result.get("IntVal")

            # ✅ PAN ni masklash
            masked_pan = (
                f"{card_pan[:6]}******{card_pan[-4:]}"
                if len(card_pan) == 16
                else "****MASK ERROR"
            )

            # ✅ Bazaga saqlash (xohlasangiz active qiling)
            # Get_Balance.objects.create(
            #     card_number=masked_pan,
            #     NumVal=numval,
            #     IntVal=intval,
            #     response_id=response_id,
            #     approval_code=approval_code,
            #     result=result_status,
            # )

            parsed_data = {
                "masked_pan": masked_pan,
                "numval": numval,
                "intval": intval,
                "response_id": response_id,
                "approval_code": approval_code,
                "result": result_status,
            }

            return Response(
                {"parsed_json": parsed_data, "raw_xml": raw_xml},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"parsed_json": {"error": f"Parse error: {str(e)}"}, "raw_xml": raw_xml},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
