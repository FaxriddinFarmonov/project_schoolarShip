from django import forms

class CardRequestForm(forms.Form):
    card_ext_rid = forms.CharField(
        label="Karta ExtRid",
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
