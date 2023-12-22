from django.db import models
from .auth import User
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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
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

class ServiceDoc(models.Model):
    doc  = models.ForeignKey(User,on_delete=models.CASCADE ,limit_choices_to = {
        "ut" :3
    })


    def __str__(self):
        return f"{self.doc.name}"

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
