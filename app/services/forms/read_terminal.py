from django import forms

class TerminalReadForm(forms.Form):
    terminal_name = forms.CharField(
        max_length=100,
        label="Terminal Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "masalan: PC044608"})
    )
