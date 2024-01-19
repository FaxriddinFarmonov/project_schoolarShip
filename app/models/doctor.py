from django.db import models
from app.models.auth import *
import datetime



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


class Teacher_info(models.Model):
    teacher_id = models.CharField(max_length=250,unique=True,blank=True,null=True)
    kafedra = models.ForeignKey(Kafedra,on_delete=models.CASCADE,blank=True,null=True)

class Graph(models.Model):
    teacher_info = models.ForeignKey(Teacher_info,on_delete=models.CASCADE,blank=True, null=True)
    citations = models.CharField(max_length=10, blank=True, null=True)
    year = models.CharField(max_length=20,blank=True, null=True)

class Cited_by(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    teacher_info = models.ForeignKey(Teacher_info,on_delete=models.CASCADE,blank=True, null=True)
    citations = models.CharField(max_length=10, blank=True, null=True)
    h_index = models.CharField(max_length=10, blank=True, null=True)
    i10_index = models.CharField(max_length=10, blank=True, null=True)
    since_2019c = models.CharField(max_length=20, blank=True, null=True)
    since_2019h = models.CharField(max_length=20, blank=True, null=True)
    since_2019h10 = models.CharField(max_length=20, blank=True, null=True)
    graph = models.ForeignKey(Graph,on_delete=models.CASCADE,blank=True,null=True)








# class ServiceDoc(models.Model):
#     doc  = models.ForeignKey(User,on_delete=models.CASCADE ,limit_choices_to = {
#         "ut" :3
#     })
#
#
#     def __str__(self):
#         return f"{self.doc.name}"

# class Rating(models.Model):
#     # user = models.ForeignKey(User ,on_delete=models.SET_NULL)
#     # doc = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     star = models.SmallIntegerField(choices=[
#         (1, " * "),
#         (2, " ** "),
#         (3, " *** "),
#         (4, " **** "),
#         (5, " ***** "),
#     ])
#     feed = models.TextField()
