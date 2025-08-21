from django import forms
from app.models.create_card import CardModify

from django import forms
from app.models.create_card import CardModify

class CardModifyForm(forms.ModelForm):
    class Meta:
        model = CardModify
        fields = ["extrid", "contract2rid", "cur_branch_code"]
        widgets = {
            "extrid": forms.TextInput(attrs={"class": "form-control", "placeholder": "ExtRid"}),
            "product_rid": forms.TextInput(attrs={"class": "form-control", "placeholder": "ProductRid"}),
            "create_contract_type_rid": forms.TextInput(attrs={"class": "form-control", "placeholder": "CreateContractTypeRid"}),
            "contract2rid": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contract2Rid"}),
            "cur_branch_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "CurBranchCode"}),
        }
