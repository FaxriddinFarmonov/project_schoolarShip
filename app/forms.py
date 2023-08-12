from django import forms

from app.models import Service, Price


class ServiceForm(forms.ModelForm):

    class Meta:
        fields = "__all__"
        model = Service


class PriceForm(forms.ModelForm):

    class Meta:
        fields = "__all__"
        model = Price