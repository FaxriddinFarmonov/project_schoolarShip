from django.contrib import admin

from app.models import CardRestriction
from app.models.doctor import *
from app.models.create_schot import LinkSchot
from app.models.create_customer import SubjectUpdate
from app.models.auth import *
from app.models.get_card import CardInfo
from app.models.read_terminal import TerminalRead
from app.models.upload_file import UploadedFile
from app.models.get_terminals import TerminalInfo


admin.site.register(User)
admin.site.register(Kafedra)
admin.site.register(OTP)
admin.site.register(Spam)
admin.site.register(Get_Balance)
admin.site.register(BlockCard)
admin.site.register(CardActivation)
admin.site.register(BalanceUpdate)
admin.site.register(SubjectUpdate)
admin.site.register(LinkSchot)
admin.site.register(UploadedFile)
admin.site.register(CardInfo)
admin.site.register(TerminalInfo)
admin.site.register(TerminalRead)
admin.site.register(CardRestriction)

# admin.site.register(Teacher_info)
# admin.site.register(Teacher_scopus)
# admin.site.register(Cited_by)
# admin.site.register(Cited_by_Scopus)
# admin.site.register(Graph)
# admin.site.register(Graph_Scoupus)
# admin.site.register(Books)
