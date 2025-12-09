import xml.etree.ElementTree as ET
import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.urls import reverse

import xml.etree.ElementTree as ET

def parse_incoming_xml(xml_text):
    tree = ET.fromstring(xml_text)

    # CustomerInfo
    client_b = tree.findtext(".//CLIENT_B")
    person_code = tree.findtext(".//PERSON_CODE")
    serial_no = tree.findtext(".//SERIAL_NO")
    id_card = tree.findtext(".//ID_CARD")
    surname = tree.findtext(".//SURNAME")
    first_name = tree.findtext(".//F_NAMES")
    sex = tree.findtext(".//SEX")
    birth_date = tree.findtext(".//B_DATE")
    mobile = tree.findtext(".//R_MOB_PHONE")

    # Address
    home_flat = tree.findtext(".//APARTMENT")
    home_house = tree.findtext(".//HOME_NUMBER")
    home_street = tree.findtext(".//STREET1")
    home_city = tree.findtext(".//R_CITY")
    home_country = tree.findtext(".//R_CNTRY")
    home_pcode = tree.findtext(".//R_PCODE")
    home_street2 = tree.findtext(".//R_STREET")

    # AgreementInfo
    contract = tree.findtext(".//CONTRACT")
    bincod = tree.findtext(".//BINCOD")
    bank_code = tree.findtext(".//BANK_CODE")
    branch = tree.findtext(".//BRANCH")
    ccy = tree.findtext(".//CCY")
    if ccy == "UZS":
        ccy_code = "D860"
    elif ccy == "USD":
        ccy_code = "D840"
    else:
        ccy_code = ccy if ccy else "D860"
    card_acct = tree.findtext(".//CARD_ACCT")

    # CardInfo
    card_pan = tree.findtext(".//U_FIELD8")
    card_name = tree.findtext(".//CARD_NAME")

    return {
        # Customer
        "rid": client_b,
        "inn": person_code,
        "passport": f"{serial_no}{id_card}" if serial_no and id_card else "",
        "last_name": surname,
        "first_name": first_name,
        "gender": "Male" if sex == "1" else "Female" if sex == "2" else "",
        "marital_status": "S",
        "birth_date": birth_date,
        "question": "yoqtirgan sporting",
        "answer": "futbool",
        "mobile": mobile,

        # Address
        "home_flat": home_flat,
        "home_house": home_house,
        "home_street": home_street,
        "home_city": home_city,
        "home_country": home_country,
        "home_pcode": home_pcode,
        "home_street2": home_street2,

        # Agreement
        "contract": contract,
        "bincod": bincod,
        "bank_code": bank_code,
        "branch": branch if branch else "10725",  # default
        "ccy": ccy_code,
        "card_acct": card_acct,

        # Card
        "card_pan": card_pan,
        "card_holder": card_name,
        "income": "100"  # default
    }


class CustomerWorkflow:
    def __init__(self, soap_url):
        self.soap_url = soap_url
        self.headers = {"Content-Type": "text/xml; charset=utf-8"}
        self.results = {}

    def create_customer(self, data):
        # Kelayotgan birth_date format: 1999-11-12T00:00:00
        raw_birth_date = data.get("birth_date", "")
        birth_date = ""
        if raw_birth_date:
            birth_date = raw_birth_date.split("T")[0]  # faqat sanani olish: 1999-11-12

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
                        <sub:Rid>{data['rid']}</sub:Rid>
                        <sub:SubjectDocuments>
                          <sub:Document TypeRid="INN" Rid="{data['inn']}" />
                          <sub:Document TypeRid="PASSPORT" Rid="{data['passport']}" />
                        </sub:SubjectDocuments>
                        <sub:AuthQAs>
                          <sub:AuthQA>
                            <tran1:Question>{data['question']}</tran1:Question>
                            <tran1:Answer>{data['answer']}</tran1:Answer>
                          </sub:AuthQA>
                        </sub:AuthQAs>
                        <sub:LastName>{data['last_name'].capitalize()}</sub:LastName>
                        <sub:LastNameLat>{data['last_name'].capitalize()}</sub:LastNameLat>
                        <sub:FirstName>{data['first_name'].capitalize()}</sub:FirstName>
                        <sub:FirstNameLat>{data['first_name'].capitalize()}</sub:FirstNameLat>
                        <sub:MiddleName>{data['first_name'].capitalize()}</sub:MiddleName>
                        <sub:Gender>{data['gender']}</sub:Gender>
                        <sub:MaritalStatus>{data['marital_status']}</sub:MaritalStatus>
                        <sub:BirthDate>{birth_date}T00:00:00+05:00</sub:BirthDate>
                        <sub:BirthName>{data['first_name'].capitalize()}</sub:BirthName>
                        <sub:EducationTypeRid>higher</sub:EducationTypeRid>
                        <sub:HomeAddress Fax="" Phone="{data['mobile']}" Flat="" Building="" House="" StreetTitle="" CityTitle="" CountryId="860" />
                        <sub:Emails><sub:Email></sub:Email></sub:Emails>
                        <sub:MobilePhones><sub:MobilePhone>{data['mobile']}</sub:MobilePhone></sub:MobilePhones>
                        <sub:WorkPhones><sub:WorkPhone>{data['mobile']}</sub:WorkPhone></sub:WorkPhones>
                        <sub:Income>100</sub:Income>
                      </sub:Person>
                    </tran:Subject>
                  </tran:Admin>
                </tran:Specific>
              </tran:Request>
            </tw:Tran>
          </soap:Body>
        </soap:Envelope>"""

        response = requests.post(self.soap_url, data=xml_data.encode("utf-8"), headers=self.headers)
        self.results["customer"] = response.text
        return self.results["customer"]

    def create_contract(self, data):
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
                    <tran:Contract Rid="{data['card_acct']}">
                      <BranchCode>{data['branch']}</BranchCode>
                      <TypeRid>{data['ccy']}</TypeRid>
                      <ClientRid>{data['rid']}</ClientRid>
                    </tran:Contract>
                  </tran:Admin>
                </tran:Specific>
              </tran:Request>
            </tw:Tran>
          </soap:Body>
        </soap:Envelope>"""

        response = requests.post(self.soap_url, data=xml_data.encode("utf-8"), headers=self.headers)
        self.results["contract"] = response.text
        return self.results["contract"]

    def create_card(self, data):
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
                    <ExtRid>{data['rid']}</ExtRid>
                    <ContractRid>{data['rid']}</ContractRid>
                    <ProductRid>VisaNEWBIN</ProductRid>
                    <CreateContractTypeRid>42403293</CreateContractTypeRid>
                    <CreateContractClientRid>{data['rid']}</CreateContractClientRid>
                    <CreateContractOutLinks>
                      <Link Kind="Access" Contract2Rid="{data['contract']}">
                        <con:Status>A</con:Status>
                      </Link>
                    </CreateContractOutLinks>
                    <CurBranchCode>{data['branch']}</CurBranchCode>
                    <DeliveryBranchCode>{data['branch']}</DeliveryBranchCode>
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
        response = requests.post(self.soap_url, data=xml_data.encode("utf-8"), headers=headers)

        self.results["card"] = response.text
        return self.results["card"]

    def run(self, parsed_data):
        customer_res = self.create_customer(parsed_data)
        contract_res = self.create_contract(parsed_data)
        card_res = self.create_card(parsed_data)

        return {
            "customer": customer_res,
            "contract": contract_res,
            "card": card_res
        }

def handle_request(xml_from_postman):
    parsed = parse_incoming_xml(xml_from_postman)
    cw = CustomerWorkflow("http://172.31.77.12:10011")
    result = cw.run(parsed)
    return result
