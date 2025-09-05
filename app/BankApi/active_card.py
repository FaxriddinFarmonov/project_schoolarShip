import xml.etree.ElementTree as ET
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.BankSerializer.active_cardSer import CardActivationSerializer
from app.models import BlockCard


def mask_card_number(pan):
    if len(pan) >= 10:
        return pan[:6] + '*' * (len(pan) - 10) + pan[-4:]
    return pan


@api_view(["POST"])
def activate_card_api(request):
    """
    Kartani aktivatsiya qilish API (ModifyToken)
    """
    serializer = CardActivationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    card_pan = serializer.validated_data["card_pan"]
    masked_pan = mask_card_number(card_pan)

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
              <Card Pan="{card_pan}" FindByPan="true">
                <Status>Active</Status>
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
        response = requests.post(
            "http://172.31.77.12:10011",
            data=xml_data.encode("utf-8"),
            headers=headers,
            timeout=30
        )

        tree = ET.fromstring(response.text)
        body = tree.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")

        fault = body.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Fault")
        if fault is not None:
            response_message = fault.findtext("faultstring", default="Nomaʼlum xatolik")

            BlockCard.objects.create(
                card_number=masked_pan,
                status="Xatolik",
                response_message=response_message
            )

            return Response({
                "status": "error",
                "message": response_message,
                "raw_response": response.text
            }, status=status.HTTP_400_BAD_REQUEST)

        # 🧩 Namespaces
        ns = {
            'soap': "http://schemas.xmlsoap.org/soap/envelope/",
            'tran': "http://schemas.tranzaxis.com/tran.xsd",
            'tok': "http://schemas.tranzaxis.com/tokens-admin.xsd"
        }

        response_tag = body.find(".//tran:Response", ns)
        token_tag = body.find(".//tok:CardVsdc", ns)

        response_id = response_tag.attrib.get("Id", "") if response_tag is not None else ""
        approval_code = response_tag.attrib.get("ApprovalCode", "") if response_tag is not None else ""
        result_status = response_tag.attrib.get("Result", "") if response_tag is not None else ""
        card_id = token_tag.attrib.get("Id", "") if token_tag is not None else ""
        response_message = "Karta aktivatsiya qilindi ✅"

        # BlockCard.objects.create(
        #     card_number=masked_pan,
        #     status="Active",
        #     response_message=response_message,
        #     response_id=response_id,
        #     approval_code=approval_code,
        #     card_id=card_id,
        #     result=result_status
        # )

        return Response({
            "status": "success" if result_status.lower() == "approved" else "error",
            "response_id": response_id,
            "approval_code": approval_code,
            "result": result_status,
            "card_id": card_id,
            "raw_response": response.text
        }, status=status.HTTP_200_OK if result_status.lower() == "approved" else status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        BlockCard.objects.create(
            card_number=masked_pan,
            status="Xatolik",
            response_message=str(e)
        )
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
