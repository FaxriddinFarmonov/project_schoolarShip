from django import forms

from app.models import Kafedra
from app.models.create_schot import LinkSchot


class KafedraForm(forms.ModelForm):

    class Meta:
        fields = ['name']
        model =Kafedra


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

# upload_form.py
# upload_form.py


from django import forms

class CardPanForm(forms.Form):
    card_pan = forms.CharField(
        max_length=16,
        min_length=16,
        label="CARD PAN",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '16 xonali karta raqami'})
    )




class BlockCardForm(forms.Form):
    card_pan = forms.CharField(
        max_length=16,
        min_length=16,
        label="CARD PAN",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '16 xonali karta raqami'
        })
    )



class CardActivationForm(forms.Form):
    card_number = forms.CharField(label="Card Number", max_length=20)




from django import forms
from .models import BalanceUpdate

from django import forms

class BalanceUpdateForm(forms.Form):
    contract_rid = forms.CharField(
        label="Contract RID",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contract RID'})
    )

    currency = forms.ChoiceField(
        choices=[('860', 'UZS'), ('840', 'USD')],
        label="Valyuta (CCY)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    balance = forms.DecimalField(
        label="Balans summasi",
        max_digits=20,
        decimal_places=4,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 1000.0000'})
    )



# upload_form.py


#
# class SubjectUpdateForm(forms.Form):
#     rid = forms.CharField(label="Subject RID", max_length=30)  # <-- shu satr bo‘lishi shart
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)
#     middle_name = forms.CharField(max_length=100, required=False)
#     birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     gender = forms.ChoiceField(choices=[('M', 'Erkak'), ('F', 'Ayol')])
#     birth_place = forms.CharField(max_length=100)
#     mobile = forms.CharField(max_length=20)
#     email = forms.EmailField()
#     income = forms.DecimalField(max_digits=15, decimal_places=2)
#     inn = forms.CharField(label="INN", max_length=20)
#     passport = forms.CharField(label="Passport", max_length=20)


# upload_form.py

from django import forms

# upload_form.py

from django import forms

class SubjectUpdateForm(forms.Form):
    rid = forms.CharField(label="Subject RID", max_length=30)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', 'Erkak'), ('F', 'Ayol')])
    marital_status = forms.ChoiceField(choices=[('M', 'Uylangan'), ('S', 'Bo‘ydoq')])
    #
    # birth_place = forms.CharField(max_length=100)
    # birth_name = forms.CharField(max_length=100)
    # residence_country_id = forms.CharField(max_length=10)
    #
    #
    home_flat = forms.CharField(max_length=10)
    home_building = forms.CharField(max_length=50)
    home_house = forms.CharField(max_length=50)
    #
    home_street = forms.CharField(max_length=100)
    home_city = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=20)
    #
    email = forms.EmailField()
    income = forms.DecimalField(max_digits=15, decimal_places=2)
    inn = forms.CharField(label="INN", max_length=20)

    passport = forms.CharField(label="Passport", max_length=20)
    # is_vip = forms.BooleanField(required=False)
    question = forms.CharField(label="Savol", max_length=255)

    answer = forms.CharField(label="javob", max_length=255)



# upload_form.py
from django import forms
from app.models.create_customer import  SubjectUpdate
from django import forms
from app.models.create_schot import LinkSchot


class LinkSchotForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=SubjectUpdate.objects.all(),
        label="Mijoz (Ism Familya)",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    BranchCode = forms.CharField(
        label="Branch Code",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = LinkSchot
        fields = ['customer', 'TypeRid', 'ClientRid', 'Rid']  # BranchCode modeli bilan bog‘liq emas, shuning uchun bu yerga yozilmaydi
        widgets = {
            'TypeRid': forms.TextInput(attrs={'class': 'form-control'}),
            'ClientRid': forms.HiddenInput(),  # Avtomatik to‘ladi
            'Rid': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ClientRid'].required = False  # Foydalanuvchi kiritmaydi

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get("customer")
        if customer:
            cleaned_data["ClientRid"] = customer.rid  # avtomatik to‘ldiramiz
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        customer = self.cleaned_data.get("customer")
        if customer:
            instance.ClientRid = customer.rid
        if commit:
            instance.save()
        return instance
