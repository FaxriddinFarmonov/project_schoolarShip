from django import forms

from app.models import Kafedra,Teacher_info,Teacher_scopus


class KafedraForm(forms.ModelForm):

    class Meta:
        fields = ['name']
        model =Kafedra


class Teacher_infoForm(forms.ModelForm):

    class Meta:
        fields = ['teacher_id_scholar','kafedra']
        model = Teacher_info
class Teacher_scopusForm(forms.ModelForm):

    class Meta:
        fields = ['name','teacher_id_scopus','kafedra']
        model = Teacher_scopus

