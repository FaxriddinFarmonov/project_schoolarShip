from django import forms

from app.models import Kafedra


class KafedraForm(forms.ModelForm):

    class Meta:
        fields = ['name']
        model =Kafedra

#
# class Teacher_infoForm(forms.ModelForm):
#
#     class Meta:
#         fields = ['teacher_id_scholar','kafedra']
#         model = Teacher_info


# class Teacher_scopusForm(forms.ModelForm):
#
#     class Meta:
#         fields = ['card_pan']


from django import forms
#
# class Teacher_scopusForm(forms.Form):
#     card_pan = forms.CharField(max_length=16, label="CARD PAN")

# forms.py
# forms.py


from django import forms

class CardPanForm(forms.Form):
    card_pan = forms.CharField(
        max_length=16,
        min_length=16,
        label="CARD PAN",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '16 xonali karta raqami'})
    )

