# app/views.py
import requests
import xml.etree.ElementTree as ET
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.BankSerializer.create_cardSer   import ModifyCardSerializer

@api_view(["POST"])
def modify_card_api(request):
    """
    Kartani o'zgartirish (ModifyToken) API
    """

    serializer = ModifyCardSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    extrid = serializer.validated_data["extrid"]
    contract2rid = serializer.validated_data["contract2rid"]
    cur_branch_code = serializer.validated_data["cur_branch_code"]

    # SOAP XML yasash
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
          <tran:Admin>
            <tran:Token>
              <Card>
                <ExtRid>{extrid}</ExtRid>
                <ContractRid>{extrid}</ContractRid>
                <ProductRid>VisaNEWBIN</ProductRid>
                <CreateContractTypeRid>42403293</CreateContractTypeRid>
                <CreateContractClientRid>{extrid}</CreateContractClientRid>
                <CreateContractOutLinks>
                  <Link Kind="Access" Contract2Rid="{contract2rid}">
                    <con:Status>A</con:Status>
                  </Link>
                </CreateContractOutLinks>
                <CurBranchCode>{cur_branch_code}</CurBranchCode>
                <DeliveryBranchCode>{cur_branch_code}</DeliveryBranchCode>
                <LifePhaseRid>New</LifePhaseRid>
              </Card>
            </tran:Token>
          </tran:Admin>
        </tran:Specific>
      </tran:Request>
    </tw:Tran>
  </soap:Body>
</soap:Envelope>"""

    headers = {"Content-Type": "text/xml; charset=utf-8"}

    try:
        response = requests.post(
            "http://172.31.77.12:10011",
            data=xml_data.encode("utf-8"),
            headers=headers,
            timeout=30
        )

        tree = ET.fromstring(response.text)
        ns = {
            "soap": "http://schemas.xmlsoap.org/soap/envelope/",
            "tran": "http://schemas.tranzaxis.com/tran.xsd",
            "tok": "http://schemas.tranzaxis.com/tokens-admin.xsd"
        }

        # SOAP ichidagi fault tekshirish
        fault = tree.find(".//soap:Fault", ns)
        if fault is not None:
            return Response({
                "status": "error",
                "fault_code": fault.findtext("faultcode", default=""),
                "fault_string": fault.findtext("faultstring", default=""),
                "raw_response": response.text
            }, status=status.HTTP_400_BAD_REQUEST)

        # Response ni olish
        response_tag = tree.find(".//tran:Response", ns)
        approval_code = response_tag.attrib.get("ApprovalCode", "") if response_tag is not None else None
        result = response_tag.attrib.get("Result", "") if response_tag is not None else None
        response_id = response_tag.attrib.get("Id", "") if response_tag is not None else None
        decline_reason = response_tag.attrib.get("DeclineReason", "") if response_tag is not None else None

        cardvsdc = tree.find(".//tok:CardVsdc", ns)
        cardvsdc_id = cardvsdc.attrib.get("Id", "") if cardvsdc is not None else None

        # 🔥 Result ni tekshiramiz
        if result and result.lower() == "approved":
            return Response({
                "status": "success",
                "response_id": response_id,
                "result": result,
                "approval_code": approval_code,
                "cardvsdc_id": cardvsdc_id,
                "raw_response": response.text
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "response_id": response_id,
                "result": result,
                "decline_reason": decline_reason,
                "approval_code": approval_code,
                "raw_response": response.text
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
