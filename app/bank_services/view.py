from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.bank_services.createCCHCard import handle_request


@csrf_exempt
def soap_handler_view(request):
    if request.method == "POST":
        xml_from_postman = request.body.decode("utf-8")  # Postmandan XML keladi
        result = handle_request(xml_from_postman)  # Sizning funksiyangizni chaqiramiz
        return JsonResponse(result, safe=False)  # Natijani JSON qaytaramiz

    return JsonResponse({"error": "Only POST allowed"}, status=405)
