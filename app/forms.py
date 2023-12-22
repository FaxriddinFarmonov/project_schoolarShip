from django import forms

from app.models import Kafedra


class KafedraForm(forms.ModelForm):

    class Meta:
        fields = "__all__"
        model =Kafedra


# class PriceForm(forms.ModelForm):
#
#     class Meta:
#         fields = "__all__"
#         model = Price