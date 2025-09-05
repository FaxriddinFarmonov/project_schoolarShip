import requests
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


SOAP_TEMPLATE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:tran="http://schemas.tranzaxis.com/tran.wsdl"
 xmlns:tran1="http://schemas.tranzaxis.com/tran.xsd">
   <soapenv:Header/>
   <soapenv:Body>
      <tran:Tran>
         <tran1:Request InitiatorRid="TURON"
                        ProcessorInstId="41"
                        OriginatorInstId="41"
                        Kind="GetTerminalInfo"
                        LifePhase="Single"
                        IsAdvice="false">
            <tran1:Parties>
               <tran1:Term Id="108" Rid="POS120"/>
            </tran1:Parties>
            <tran1:Specific>
               <tran1:CustInfo 
                   Kinds="TerminalId TerminalContractId TerminalInstId TerminalClassGuid TerminalClassTitle TerminalExtRid
                          TerminalName TerminalTitle TerminalStatus TerminalStatusTitle TerminalOwnerMcc TerminalDfltCcy TerminalAddress
                          TerminalAddressLatitude TerminalAddressLongitude TerminalDistance TerminalCassetteInfo TerminalStateConnected TerminalAcceptCash"
                   Language="en"/>
            </tran1:Specific>
         </tran1:Request>
      </tran:Tran>
   </soapenv:Body>
</soapenv:Envelope>
"""


class TerminalLookupAPIView(APIView):
    def post(self, request):
        headers = {"Content-Type": "text/xml;charset=UTF-8"}
        url = "http://172.31.77.12:10011"

        try:
            response = requests.post(
                url, data=SOAP_TEMPLATE.encode("utf-8"), headers=headers, timeout=15
            )
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        raw_xml = response.text

        try:
            tree = ET.fromstring(raw_xml)
            body = tree.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")

            # SOAP Fault check
            fault = body.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Fault")
            if fault is not None:
                parsed_data = {
                    "error": fault.findtext("faultstring", default="Nomaʼlum xatolik")
                }
                return Response(
                    {"parsed_json": parsed_data, "raw_xml": raw_xml},
                    status=status.HTTP_200_OK,
                )

            # XML parsing → JSON
            ns = {
                "tran": "http://schemas.tranzaxis.com/tran.xsd",
                "tran1": "http://schemas.tranzaxis.com/tran-common.xsd",
            }

            parsed_json = []
            for item in tree.findall(".//tran1:Item", ns):
                current_data = {}
                for attr in item.findall("tran1:Attribute", ns):
                    kind = attr.attrib.get("Kind")
                    # barcha qiymatlarni tekshirib yig‘amiz
                    val = (
                        attr.findtext("tran1:IntVal", namespaces=ns)
                        or attr.findtext("tran1:StrVal", namespaces=ns)
                        or attr.findtext("tran1:BoolVal", namespaces=ns)
                        or attr.findtext("tran1:NumVal", namespaces=ns)
                        or ""
                    )
                    current_data[kind] = val
                if current_data:
                    parsed_json.append(current_data)

            return Response(
                {"parsed_json": parsed_json, "raw_xml": raw_xml},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"parsed_json": {"error": f"Parse error: {str(e)}"}, "raw_xml": raw_xml},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
