# app/api_views/limit_card_api.py
import requests
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models.limit_card import CardRestriction
from app.BankSerializer.remove_limitSer import CardLimitRemoveSerializer


class CardLimitRemoveAPIView(APIView):
    def post(self, request):
        serializer = CardLimitRemoveSerializer(data=request.data)
        if serializer.is_valid():
            card_number = serializer.validated_data['card_number']

            # SOAP so‘rov
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
                                       <tok:Restriction>
                                          <res:Rid>EXTID_CARD_RESTRICTION</res:Rid>
                                          <res:ToDelete>true</res:ToDelete>
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

            try:
                response = requests.post("http://172.31.77.12:10011", data=soap_body, headers=headers, timeout=20)

                # Javobni XML dan parse qilish
                tree = ET.fromstring(response.text)
                ns = {
                    "tran": "http://schemas.tranzaxis.com/tran.xsd",
                    "tok": "http://schemas.tranzaxis.com/tokens-admin.xsd",
                }

                response_node = tree.find(".//tran:Response", ns)
                if response_node is not None:
                    result = response_node.attrib.get("Result")
                    approval_code = response_node.attrib.get("ApprovalCode")
                else:
                    result, approval_code = "Failed", None

                card_id = tree.find(".//tok:CardVsdc", ns).attrib.get("Id") if tree.find(".//tok:CardVsdc", ns) is not None else None
                restriction_guid = tree.find(".//tok:Restriction", ns).attrib.get("Guid") if tree.find(".//tok:Restriction", ns) is not None else None

                # Maskalash funksiyasi
                def mask_card_number(num):
                    return num[0:4] + "*" * (len(num) - 8) + num[-4:]

                # Statusni aniqlash
                if result == "Approved":
                    status_value = "No Limit"
                else:
                    status_value = "Failed"

                # Modelga yozish
                # CardRestriction.objects.create(
                #     card_number=mask_card_number(card_number),
                #     result=result,
                #     approval_code=approval_code,
                #     card_id=card_id,
                #     restriction_guid=restriction_guid,
                #     status=status_value
                # )

                return Response({
                    "request_data": serializer.data,
                    "soap_response": response.text,  # 🔥 tashqi serverdan qaytgan XML javob
                    "parsed": {
                        "result": result,
                        "approval_code": approval_code,
                        "card_id": card_id,
                        "restriction_guid": restriction_guid,
                        "status": status_value
                    }
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
