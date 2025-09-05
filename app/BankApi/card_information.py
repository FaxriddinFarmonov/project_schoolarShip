import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from xml.etree import ElementTree as ET
from app.BankSerializer.card_informationSer import CardLookupSerializer


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


def etree_to_dict(element):
    """XML elementni rekursiv JSON dict ga aylantiradi"""
    node = {}

    # agar atributlari bo‘lsa qo‘shamiz
    if element.attrib:
        for k, v in element.attrib.items():
            node[f"@{k}"] = v

    # agar childlari bo‘lsa rekursiv o‘qiymiz
    children = list(element)
    if children:
        for child in children:
            tag = child.tag.split("}")[-1]  # namespace olib tashlanadi
            child_dict = etree_to_dict(child)
            if tag in node:
                # agar tag ko‘p marta uchrasa -> list qilamiz
                if not isinstance(node[tag], list):
                    node[tag] = [node[tag]]
                node[tag].append(child_dict)
            else:
                node[tag] = child_dict
    else:
        # leaf element -> text qiymatini qo‘yamiz
        text = element.text.strip() if element.text else None
        if text:
            node["#text"] = text

    return node


class CardLookupAPIView(APIView):
    def post(self, request):
        serializer = CardLookupSerializer(data=request.data)
        if serializer.is_valid():
            card_ext_rid = serializer.validated_data["card_ext_rid"]

            soap_body = SOAP_TEMPLATE.format(card_ext_rid=card_ext_rid)
            headers = {"Content-Type": "text/xml; charset=utf-8"}
            url = "http://172.31.77.12:10011"

            try:
                response = requests.post(
                    url, data=soap_body.encode("utf-8"), headers=headers, timeout=10
                )
            except requests.exceptions.RequestException as e:
                return Response(
                    {"error": str(e), "raw_response": None},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            raw_xml = response.text  # tashqi serverdan kelgan XML

            try:
                tree = ET.fromstring(raw_xml)

                # XML -> JSON (rekursiv)
                xml_as_json = etree_to_dict(tree)

                # doim ham JSON, ham XML qaytadi
                return Response(
                    {"parsed_response": xml_as_json, "raw_response": raw_xml},
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                return Response(
                    {"error": f"Parse error: {str(e)}", "raw_response": raw_xml},
                    status=status.HTTP_200_OK,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
