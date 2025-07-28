from django.db import models
from app.models.auth import *
from datetime import datetime



class Kafedra(models.Model):
    name = models.CharField(max_length=512)
    about = models.CharField(max_length=500)


    class Meta:
        verbose_name_plural = "2. Kafedra"
        verbose_name = "Kafedra"
    def __str__(self):
        return f"{self.name}"





class Spam(models.Model):

    date = models.DateTimeField(auto_now=True,blank=True,null = True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.name
    def save(self,*args,**kwargs):
        try:
            self.user.is_spam = True
            self.user.save()
        except:
            pass

        if not self.date:
            now = datetime.datetime.now()
            minut = 5+now.minute
            soat = now.hour
            if minut >59:
                minut = minut-60
                soat+=1
            if minut // 10 <1:
                minut = '0'+str(minut)

            self.date = datetime.datetime.now().strftime(f"%Y-%m-%d {soat}:{minut}:%S.%f")
        return super(Spam,self).save(*args,**kwargs)

#
# class Teacher_info(models.Model):
#     name = models.CharField(max_length=250, blank=True, null=True)
#     teacher_id_scholar = models.CharField(max_length=250,unique=True,blank=True,null=True)
#     kafedra = models.ForeignKey(Kafedra,on_delete=models.CASCADE,blank=True,null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.name}"
#
# class Graph(models.Model):
#         name = models.CharField(max_length=250, blank=True, null=True)
#         teacher_info = models.ForeignKey(Teacher_info, on_delete=models.CASCADE, blank=True, null=True)
#         title = models.CharField(max_length=1000, blank=True, null=True)
#         value = models.CharField(max_length=1000, blank=True, null=True)
#         year = models.CharField(max_length=100, blank=True, null=True)
#         links = models.CharField(max_length=2000, blank=True, null=True)
#         publication = models.CharField(max_length=2000, blank=True, null=True)
#
#
#
#
# class Cited_by(models.Model):
#         name = models.CharField(max_length=250, blank=True, null=True)
#         teacher_info = models.ForeignKey(Teacher_info,on_delete=models.CASCADE,blank=True, null=True)
#         citations = models.CharField(max_length=10, blank=True, null=True)
#         h_index = models.CharField(max_length=10, blank=True, null=True)
#         i10_index = models.CharField(max_length=10, blank=True, null=True)
#         since_2019c = models.CharField(max_length=20, blank=True, null=True)
#         since_2019h = models.CharField(max_length=20, blank=True, null=True)
#         since_2019h10 = models.CharField(max_length=20, blank=True, null=True)
#         graph = models.ForeignKey(Graph,on_delete=models.CASCADE,blank=True,null=True)
#
#
#         def __str__(self):
#             return f"{self.name}"
#
# class Teacher_scopus(models.Model):
#     name = models.CharField(max_length=250, blank=True, null=True)
#     teacher_id_scopus = models.CharField(max_length=250,unique=True,blank=True,null=True)
#     kafedra = models.ForeignKey(Kafedra,on_delete=models.CASCADE,blank=True,null=True)
#     def __str__(self):
#         return f"{self.name}"
#
#
#
#
#
# class Graph_Scoupus(models.Model):
#     name = models.CharField(max_length=250, blank=True, null=True)
#     teacher_scopus = models.ForeignKey(Teacher_scopus,on_delete=models.CASCADE,blank=True, null=True)
#     title = models.CharField(max_length=1000,blank=True, null=True)
#     value = models.CharField(max_length=1000,blank=True, null=True)
#     year = models.CharField(max_length=100,blank=True, null=True)
#     links = models.CharField(max_length=2000,blank=True, null=True)
#     publication = models.CharField(max_length=2000,blank=True, null=True)
#     def __str__(self):
#         return f"{self.name}"
#
#
# class Cited_by_Scopus(models.Model):
#     name = models.CharField(max_length=250, blank=True, null=True)
#     teacher_scopus = models.ForeignKey(Teacher_scopus,on_delete=models.CASCADE,blank=True, null=True)
#     citations = models.CharField(max_length=10, blank=True, null=True)
#     h_index = models.CharField(max_length=10, blank=True, null=True)
#     publications = models.CharField(max_length=10, blank=True, null=True)
#     graph_scopus = models.ForeignKey(Graph_Scoupus,on_delete=models.CASCADE,blank=True,null=True)
#
#     def __str__(self):
#         return f"{self.name}"
#
#
#
#
#
#
#
#
#
#
#
# # class ServiceDoc(models.Model):
# #     doc  = models.ForeignKey(User,on_delete=models.CASCADE ,limit_choices_to = {
# #         "ut" :3
# #     })
# #
# #
# #     def __str__(self):
# #         return f"{self.doc.name}"
#
# # class Rating(models.Model):
# #     # user = models.ForeignKey(User ,on_delete=models.SET_NULL)
# #     # doc = models.ForeignKey(Doctor, on_delete=models.CASCADE)
# #     star = models.SmallIntegerField(choices=[
# #         (1, " * "),
# #         (2, " ** "),
# #         (3, " *** "),
# #         (4, " **** "),
# #         (5, " ***** "),
# #     ])
# #     feed = models.TextField()




class Get_Balance(models.Model):
    NumVal = models.CharField(max_length=250, blank=True, null=True)
    IntVal = models.CharField(max_length=5,blank=True, null=True)
    card_number = models.CharField(max_length=32)
    date_balance = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.card_number} - - {self.NumVal}"



# models.py


class BlockCard(models.Model):
    card_number = models.CharField(max_length=32)
    status = models.CharField(max_length=32, default="Blocked")
    response_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - {self.status}"




class CardActivation(models.Model):
    ext_rid = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="Active")
    masked_card_number = models.CharField(max_length=25, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.masked_card_number} - {self.status}"
