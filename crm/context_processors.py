from django.conf import settings


def user_type(request):
   try:
        types = {
            1: "page/direct/main.html",
            2: "page/admin/main.html",
            3: "page/doc/main.html",
            4: "page/client/main.html"
        }.get(request.user.ut, "page/doc/main.html")
   except:
        types = "page/doc/main.html"

   ctx = {
       "type":types,
       "app_name":settings.APP_NAME
   }
   if not request.user.is_anonymous:
        ctx.update({'ut':request.user.ut})
   return ctx