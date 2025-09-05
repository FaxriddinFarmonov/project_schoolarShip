import requests
import xml.etree.ElementTree as ET
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.BankSerializer.P2P_cardSer import PaymentSerializer

SOAP_TEMPLATE = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:tw="http://schemas.tranzaxis.com/tran.wsdl"
 xmlns:tran="http://schemas.tranzaxis.com/tran.xsd"
 xmlns:tran1="http://schemas.tranzaxis.com/tran-common.xsd">
   <soap:Body>
      <tw:Tran>
         <tran:Request LifePhase="Single" InitiatorRid="TURON" Kind="Payment" TextMess="Remarks">
            <tran:Parties>
               <tran:Term Rid="MobileBn"/>
               <tran:Cust AuthChecked="true">
                  <tran:Token Kind="Card" ExtRid="{extrid}">
                     <tran1:Card/>
                  </tran:Token>
               </tran:Cust>
               <tran:Payee>
                  <tran1:Card Pan="{pan}"/>
               </tran:Payee>
            </tran:Parties>
            <tran:Match CheckForDuplicate="true" Key="{key}"/>
            <tran:Moneys>
               <tran:Clear Amt="{amount}" Ccy="{currency}"/>
               <tran:Cust Amt="{amount}" Ccy="{currency}"/>
            </tran:Moneys>
         </tran:Request>
      </tw:Tran>
   </soap:Body>
</soap:Envelope>"""

class PaymentAPIView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        extrid = serializer.validated_data["extrid"]
        pan = serializer.validated_data["pan"]
        amount = serializer.validated_data["amount"]
        currency = serializer.validated_data["currency"]

        # 🔑 Har safar yangi Key generatsiya qilamiz
        generated_key = uuid.uuid4().hex.upper()

        payload = SOAP_TEMPLATE.format(
            extrid=extrid,
            pan=pan,
            amount=amount,
            currency=currency,
            key=generated_key
        )

        url = "http://172.31.77.12:10011"
        headers = {"Content-Type": "text/xml; charset=utf-8"}

        try:
            resp = requests.post(url, data=payload.encode("utf-8"), headers=headers, timeout=20)
        except requests.RequestException as e:
            return Response({"error": f"UZELGA ulanib bo‘lmadi: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        raw_xml = resp.text

        # XML → JSON parse
        try:
            tree = ET.fromstring(raw_xml)
            ns = {
                "soap": "http://schemas.xmlsoap.org/soap/envelope/",
                "tran": "http://schemas.tranzaxis.com/tran.xsd"
            }

            parsed = {}
            response_el = tree.find(".//tran:Response", ns)
            if response_el is not None:
                parsed["id"] = response_el.attrib.get("Id")
                parsed["oper_day"] = response_el.attrib.get("OperDay")
                parsed["result"] = response_el.attrib.get("Result")
                parsed["approval_code"] = response_el.attrib.get("ApprovalCode")
                parsed["version"] = response_el.attrib.get("Version")
            else:
                parsed["id"] = None
                parsed["oper_day"] = None
                parsed["result"] = None
                parsed["approval_code"] = None
                parsed["version"] = None

        except Exception as e:
            return Response(
                {"error": f"XML parse xatosi: {e}", "raw_xml": raw_xml},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "parsed_json": parsed,
                "generated_key": generated_key,  # 🔑 Key ham qaytariladi
                "raw_xml": raw_xml
            },
            status=status.HTTP_200_OK,
        )
