from decimal import Decimal
import requests
import xml.etree.ElementTree as ET
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app.BankSerializer.linkshootSer import ContractUpdateSerializer


@api_view(["POST"])
def contract_update_api(request):
    serializer = ContractUpdateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    cd = serializer.validated_data
    contract_rid = cd.get('Rid')
    client_rid = cd.get('ClientRid')
    type_rid = cd.get('TypeRid')
    branch_code = cd.get('BranchCode')

    # 📨 SOAP XML
    xml_data = f"""<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <tw:Tran xmlns:tw="http://schemas.tranzaxis.com/tran.wsdl"
             xmlns:tran="http://schemas.tranzaxis.com/tran.xsd">
      <tran:Request xmlns="http://schemas.tranzaxis.com/contracts-admin.xsd"
                    xmlns:tran="http://schemas.tranzaxis.com/tran.xsd"
                    InitiatorRid="TURON"
                    LifePhase="Single"
                    Kind="ModifyContract">
        <tran:Specific>
          <tran:Admin ObjectMustExist="false">
            <tran:Contract Rid="{contract_rid}">
              <BranchCode>{branch_code}</BranchCode>
              <TypeRid>{type_rid}</TypeRid>
              <ClientRid>{client_rid}</ClientRid>
            </tran:Contract>
          </tran:Admin>
        </tran:Specific>
      </tran:Request>
    </tw:Tran>
  </soap:Body>
</soap:Envelope>"""

    headers = {"Content-Type": "text/xml; charset=utf-8"}

    try:
        # timeout qo‘ydik (read va connect)
        response = requests.post(
            "http://172.31.77.12:10011",
            data=xml_data.encode("utf-8"),
            headers=headers,
            timeout=(5, 30),
        )

        # HTTP xatoni aniq qaytaramiz
        if response.status_code != 200:
            return Response({
                "status": "error",
                "error_type": "HTTPError",
                "http_status": response.status_code,
                "message": f"HTTP {response.status_code} from SOAP endpoint",
                "raw_response": response.text[:2000],
            }, status=status.HTTP_502_BAD_GATEWAY)

        # XML parsing
        try:
            tree = ET.fromstring(response.text)
        except ET.ParseError as pe:
            return Response({
                "status": "error",
                "error_type": "XMLParseError",
                "message": str(pe),
                "raw_response": response.text[:2000],
            }, status=status.HTTP_502_BAD_GATEWAY)

        ns = {
            'soap': "http://schemas.xmlsoap.org/soap/envelope/",
            'tran': "http://schemas.tranzaxis.com/tran.xsd",
            '': "http://schemas.tranzaxis.com/contracts-admin.xsd"
        }

        body = tree.find(".//soap:Body", ns)
        if body is None:
            return Response({
                "status": "error",
                "error_type": "SOAPStructureError",
                "message": "SOAP Body topilmadi",
                "raw_response": response.text[:2000],
            }, status=status.HTTP_502_BAD_GATEWAY)

        # SOAP Fault bo‘lsa — faultcode/faultstring/ detail bilan qaytaramiz
        fault = body.find(".//soap:Fault", ns)
        if fault is not None:
            # faultcode va faultstring ba’zan namespace-siz bo‘ladi
            faultcode = fault.findtext("faultcode") or fault.findtext("soap:faultcode", namespaces=ns)
            faultstring = fault.findtext("faultstring") or fault.findtext("soap:faultstring", namespaces=ns)
            detail_elem = fault.find(".//detail") or fault.find(".//soap:detail", ns)
            detail_xml = ET.tostring(detail_elem, encoding="unicode") if detail_elem is not None else None

            return Response({
                "status": "error",
                "error_type": "SOAPFault",
                "fault_code": faultcode,
                "fault_string": faultstring,
                "detail": detail_xml,
                "raw_response": response.text[:4000],
            }, status=status.HTTP_400_BAD_REQUEST)

        # Response bor, lekin Approved emas bo‘lishi ham mumkin — biznes xato sifatida qaytaramiz
        response_tag = body.find(".//tran:Response", ns)
        if response_tag is None:
            return Response({
                "status": "error",
                "error_type": "SOAPStructureError",
                "message": "tran:Response topilmadi",
                "raw_response": response.text[:2000],
            }, status=status.HTTP_502_BAD_GATEWAY)

        result_attr = (response_tag.get("Result") or "").strip()
        approval_code = response_tag.get("ApprovalCode")

        # Contract va account
        contract_tag = body.find(".//tran:Contract", ns)
        account_tag = contract_tag.find(".//Account", ns) if contract_tag is not None else None

        # Agar Result != Approved — reason qidiramiz
        if result_attr and result_attr.lower() != "approved":
            # Ehtimoliy reason/description node-laridan birini topishga urinib ko‘ramiz
            possible_reason_tags = ["Reason", "Error", "Message", "Description"]
            reason_text = None
            for tag in possible_reason_tags:
                el = body.find(f".//tran:{tag}", ns)
                if el is not None and el.text and el.text.strip():
                    reason_text = el.text.strip()
                    break

            return Response({
                "status": "error",
                "error_type": "BusinessError",
                "result": result_attr,
                "approval_code": approval_code,
                "reason": reason_text,
                "raw_response": response.text[:4000],
            }, status=status.HTTP_400_BAD_REQUEST)

        # Approved holat — qiymatlarni yig‘amiz
        branch_name = contract_tag.findtext(".//BranchName", default="", namespaces=ns) if contract_tag is not None else ""
        branch_code_resp = contract_tag.findtext(".//BranchCode", default="", namespaces=ns) if contract_tag is not None else ""
        inst_name = contract_tag.attrib.get("InstName", "") if contract_tag is not None else ""
        contract_rid_resp = contract_tag.attrib.get("Rid", "") if contract_tag is not None else ""
        client_id = contract_tag.findtext(".//ClientId", default="", namespaces=ns) if contract_tag is not None else ""
        currency = account_tag.attrib.get("Ccy", "") if account_tag is not None else ""
        balance = account_tag.findtext(".//Balance", default="0", namespaces=ns) if account_tag is not None else "0"

        return Response({
            "status": "success",
            "result": result_attr or "Approved",
            "approval_code": approval_code,
            "contract_rid": contract_rid_resp,
            "client_id": client_id,
            "currency": currency,
            "balance": balance,
            "branch_name": branch_name,
            "branch_code": branch_code_resp,
            "inst_name": inst_name,
            "raw_response": response.text[:4000],
        }, status=status.HTTP_200_OK)

    except requests.exceptions.Timeout as e:
        return Response({
            "status": "error",
            "error_type": "Timeout",
            "message": str(e),
        }, status=status.HTTP_504_GATEWAY_TIMEOUT)

    except requests.exceptions.ConnectionError as e:
        return Response({
            "status": "error",
            "error_type": "ConnectionError",
            "message": str(e),
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    except requests.exceptions.RequestException as e:
        return Response({
            "status": "error",
            "error_type": "RequestException",
            "message": str(e),
        }, status=status.HTTP_502_BAD_GATEWAY)

    except Exception as e:
        return Response({
            "status": "error",
            "error_type": "UnhandledException",
            "message": str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
