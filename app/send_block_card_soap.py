# utils.py yoki views.py
import requests

def send_block_card_soap(card_number):
    url = "https://test.ohost.uz:9443/tokens-admin"  # O'zingizda mavjud endpoint
    headers = {
        "Content-Type": "text/xml;charset=UTF-8",
        "SOAPAction": ""
    }

    soap_body = f"""<?xml version="1.0"?>
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
                  <Card>
                    <ExtRid>{card_number}</ExtRid>
                    <Status>Blocked</Status>
                  </Card>
                </tran:Token>
              </tran:Admin>
            </tran:Specific>
          </tran:Request>
        </tw:Tran>
      </soap:Body>
    </soap:Envelope>
    """

    response = requests.post(url, data=soap_body.strip(), headers=headers, verify=False)
    return response.text
