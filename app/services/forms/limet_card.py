from django import forms

class CardRestrictionForm(forms.Form):
    card_number = forms.CharField(label="Card Number (ExtRid)", max_length=32)
    max_value = forms.DecimalField(label="Max Value", max_digits=20, decimal_places=2)
    currency = forms.CharField(label="Currency (Ccy)", max_length=10)

class CardLimitRemoveForm(forms.Form):
    card_number = forms.CharField(label="Card Number (ExtRid)", max_length=32)

