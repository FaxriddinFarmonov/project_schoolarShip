from django import forms

from app.models import Kafedra,Teacher_info


class KafedraForm(forms.ModelForm):

    class Meta:
        fields = "__all__"
        model =Kafedra


class Teacher_infoForm(forms.ModelForm):

    class Meta:
        fields = ['teacher_id','kafedra']
        model = Teacher_info