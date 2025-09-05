from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import xml.etree.ElementTree as ET
from app.BankSerializer.create_customerSer import SubjectUpdateSerializer

@api_view(["POST"])
def subject_update_api(request):
    serializer = SubjectUpdateSerializer(data=request.data)

    if serializer.is_valid():
        cd = serializer.validated_data

        # XML yasash
        xml_data = f"""<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <tw:Tran xmlns:tw="http://schemas.tranzaxis.com/tran.wsdl"
             xmlns:tran="http://schemas.tranzaxis.com/tran.xsd"
             xmlns:sub="http://schemas.tranzaxis.com/subjects-admin.xsd"
             xmlns:tran1="http://schemas.tranzaxis.com/tran-common.xsd">
      <tran:Request InitiatorRid="TURON" LifePhase="Single" Kind="ModifySubject">
        <tran:Specific>
          <tran:Admin>
            <tran:Subject>
              <sub:Person TypeRid="Cardholder">
                <sub:Rid>{cd['rid']}</sub:Rid>
                <sub:SubjectDocuments>
                  <sub:Document TypeRid="INN" Rid="{cd['inn']}" />
                  <sub:Document TypeRid="PASSPORT" Rid="{cd['passport']}" />
                </sub:SubjectDocuments>
                <sub:AuthQAs>
                  <sub:AuthQA>
                    <tran1:Question>{cd['question']}</tran1:Question>
                    <tran1:Answer>{cd['answer']}</tran1:Answer>
                  </sub:AuthQA>
                </sub:AuthQAs>
                <sub:LastName>{cd['last_name'].capitalize()}</sub:LastName>
                <sub:LastNameLat>{cd['last_name'].capitalize()}</sub:LastNameLat>
                <sub:FirstName>{cd['first_name'].capitalize()}</sub:FirstName>
                <sub:FirstNameLat>{cd['first_name'].capitalize()}</sub:FirstNameLat>
                <sub:MiddleName>{cd['first_name'].capitalize()}</sub:MiddleName>
                <sub:Gender>{cd['gender']}</sub:Gender>
                <sub:MaritalStatus>{cd['marital_status']}</sub:MaritalStatus>
                <sub:BirthDate>{cd['birth_date']}T00:00:00+05:00</sub:BirthDate>
                <sub:BirthName>{cd['first_name'].capitalize()}</sub:BirthName>
                <sub:EducationTypeRid>higer</sub:EducationTypeRid>
                <sub:HomeAddress Fax="" Phone="{cd['mobile']}" Flat="{cd['home_flat']}" Building="{cd['home_building']}" House="{cd['home_house']}" StreetTitle="{cd['home_street']}" CityTitle="{cd['home_city']}" CountryId="860" />
                <sub:Emails><sub:Email>{cd['email']}</sub:Email></sub:Emails>
                <sub:MobilePhones><sub:MobilePhone>{cd['mobile']}</sub:MobilePhone></sub:MobilePhones>
                <sub:WorkPhones><sub:WorkPhone>{cd['mobile']}</sub:WorkPhone></sub:WorkPhones>
                <sub:Income>{cd['income']}</sub:Income>
              </sub:Person>
            </tran:Subject>
          </tran:Admin>
        </tran:Specific>
      </tran:Request>
    </tw:Tran>
  </soap:Body>
</soap:Envelope>"""

        headers = {"Content-Type": "text/xml; charset=utf-8"}

        try:
            response = requests.post("http://172.31.77.12:10011", data=xml_data.encode("utf-8"), headers=headers)
            tree = ET.fromstring(response.text)

            ns = {
                'soap': "http://schemas.xmlsoap.org/soap/envelope/",
                'tran': "http://schemas.tranzaxis.com/tran.xsd",
                'sub': "http://schemas.tranzaxis.com/subjects-admin.xsd"
            }

            body = tree.find(".//soap:Body", ns)
            fault = body.find(".//soap:Fault", ns)

            if fault is not None:
                return Response({
                    "status": "error",
                    "fault": fault.findtext("faultstring", default="Nomaʼlum xatolik")
                }, status=status.HTTP_400_BAD_REQUEST)

            response_tag = body.find(".//tran:Response", ns)
            person_tag = body.find(".//sub:Person", ns)
            docs = person_tag.findall(".//sub:Document", ns)
            authqa_tag = person_tag.find(".//sub:AuthQA", ns)

            return Response({
                "status": "success",
                "approval_code": response_tag.get("ApprovalCode"),
                "response_id": response_tag.get("Id"),
                "person_id": person_tag.get("Id"),
                "doc_ids": [d.get("Id") for d in docs],
                "authqa_id": authqa_tag.get("Id") if authqa_tag is not None else None,
                "raw_response": response.text
            })

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
