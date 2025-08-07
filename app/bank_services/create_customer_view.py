from django.shortcuts import render, redirect
from django.urls import reverse
from app.forms import SubjectUpdateForm
from app.models import SubjectUpdate
import requests
import xml.etree.ElementTree as ET

def subject_update_view(request):
    form = SubjectUpdateForm()

    if request.method == 'POST':
        form = SubjectUpdateForm(request.POST)
        # print(form)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)

            # XML
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

                # 🟡 SOAP dan to‘liq javobni chiqarish
                print("\n🔵 SOAPdan to‘liq javob:\n")
                print(response.text)
                print("\n🔵 END SOAP javob\n")

                tree = ET.fromstring(response.text)
                ns = {
                    'soap': "http://schemas.xmlsoap.org/soap/envelope/",
                    'tran': "http://schemas.tranzaxis.com/tran.xsd",
                    'sub': "http://schemas.tranzaxis.com/subjects-admin.xsd"
                }

                body = tree.find(".//soap:Body", ns)
                fault = body.find(".//soap:Fault", ns)

                if fault is not None:
                    result = {"Xato": fault.findtext("faultstring", default="Nomaʼlum xatolik")}
                    print("❌ SOAP xatosi:", result["Xato"])
                else:
                    response_tag = body.find(".//tran:Response", ns)
                    person_tag = body.find(".//sub:Person", ns)
                    docs = person_tag.findall(".//sub:Document", ns)
                    authqa_tag = person_tag.find(".//sub:AuthQA", ns)

                    # 🟢 Muhim elementlarni print qilish
                    print("🟢 ApprovalCode:", response_tag.get("ApprovalCode"))
                    print("🟢 Person ID:", person_tag.get("Id"))
                    print("🟢 AuthQA ID:", authqa_tag.get("Id") if authqa_tag is not None else "Yo‘q")

                    # Ma'lumotlarni bazaga yozish
                    SubjectUpdate.objects.create(
                        rid=cd['rid'],
                        inn=cd['inn'],
                        passport=cd['passport'],

                        last_name=cd['last_name'].capitalize(),
                        # last_name_lat=cd['last_name_lat'],
                        first_name=cd['first_name'].capitalize(),

                        # first_name_lat=cd['first_name_lat'],
                        # middle_name=cd.get('middle_name', ''),
                        gender=cd['gender'],

                        marital_status=cd['marital_status'],
                        birth_date=cd['birth_date'],
                        # birth_place=cd['birth_place'],

                        # birth_name=cd['birth_name'],
                        # residence_country_id=cd['residence_country_id'],
                        # home_fax=cd['home_fax'],

                        # home_phone=cd['home_phone'],
                        home_flat=cd['home_flat'],
                        home_building=cd['home_building'],

                        home_house=cd['home_house'],
                        home_street=cd['home_street'],
                        home_city=cd['home_city'],

                        email=cd['email'],
                        mobile=cd['mobile'],
                        # work_phone=cd['work_phone'],

                        income=cd['income'],
                        # is_vip=cd['is_vip'],
                        question=cd['question'],
                        answer=cd['answer'],

                        response_id=response_tag.get("Id"),
                        approval_code=response_tag.get("ApprovalCode"),
                        person_id=person_tag.get("Id"),

                        doc_id_1=docs[0].get("Id") if len(docs) > 0 else None,
                        doc_id_2=docs[1].get("Id") if len(docs) > 1 else None,
                        authqa_id=authqa_tag.get("Id") if authqa_tag is not None else None,
                    )

                    result = {"Success": "✅ Maʼlumotlar muvaffaqiyatli saqlandi."}

                request.session["result"] = result
                request.session["soap_raw"] = response.text
                request.session["show_form"] = False

            except Exception as e:
                print("🚨 SOAP Exception:", str(e))
                request.session["result"] = {"Xatolik": str(e)}
                request.session["soap_raw"] = ""
                request.session["show_form"] = False

            return redirect(reverse("get_customers"))

    result = request.session.pop("result", None)
    soap_raw = request.session.pop("soap_raw", None)
    show_form = request.session.pop("show_form", True)

    return render(request, "page/create_customer.html", {
        "form": form,
        "result": result,
        "soap_raw": soap_raw,
        "show_form": show_form,
        "pos": "form"
    })
