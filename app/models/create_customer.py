from django.db import models
from app.models.auth import *
from datetime import datetime
from datetime import date


from django.db import models

class SubjectUpdate(models.Model):
    # Form inputlari
    rid = models.CharField(max_length=100)
    inn = models.CharField(max_length=20)
    passport = models.CharField(max_length=20)
    last_name = models.CharField(max_length=100)
    last_name_lat = models.CharField(max_length=100,blank=True,null=True)
    first_name = models.CharField(max_length=100)
    first_name_lat = models.CharField(max_length=100,blank=True,null=True)
    middle_name = models.CharField(max_length=100,blank=True,null=True)
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=20,blank=True,null=True)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100,blank=True,null=True)
    birth_name = models.CharField(max_length=100,blank=True,null=True)
    education_type_rid = models.CharField(max_length=50,blank=True,null=True)
    residence_country_id = models.CharField(max_length=10,blank=True,null=True)
    reg_flat = models.CharField(max_length=10,blank=True,null=True)
    reg_building = models.CharField(max_length=10,blank=True,null=True)
    reg_house = models.CharField(max_length=10,blank=True,null=True)
    reg_street = models.CharField(max_length=10,blank=True,null=True)
    reg_city = models.CharField(max_length=10,blank=True,null=True)
    home_fax = models.CharField(max_length=50,blank=True,null=True)
    home_phone = models.CharField(max_length=50,blank=True,null=True)
    home_flat = models.CharField(max_length=10,blank=True,null=True)
    home_building = models.CharField(max_length=10,blank=True,null=True)
    home_house = models.CharField(max_length=10,blank=True,null=True)
    home_street = models.CharField(max_length=100,blank=True,null=True)
    home_city = models.CharField(max_length=100,blank=True,null=True)
    home2_flat = models.CharField(max_length=10,blank=True,null=True)
    home2_building = models.CharField(max_length=10,blank=True,null=True)
    home2_house = models.CharField(max_length=10,blank=True,null=True)
    home2_street = models.CharField(max_length=100,blank=True,null=True)
    home2_city = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    work_phone = models.CharField(max_length=20,blank=True,null=True)
    income = models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    is_vip = models.BooleanField(default=False)

    # AuthQA
    question = models.CharField(max_length=255)

    answer = models.CharField(max_length=255)

    # SOAP javob maydonlari
    response_id = models.CharField(max_length=100, blank=True, null=True)
    approval_code = models.CharField(max_length=100, blank=True, null=True)
    person_id = models.CharField(max_length=100, blank=True, null=True)
    doc_id_1 = models.CharField(max_length=100, blank=True, null=True)
    doc_id_2 = models.CharField(max_length=100, blank=True, null=True)
    authqa_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
