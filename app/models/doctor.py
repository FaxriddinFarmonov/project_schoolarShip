from django.db import models
from .auth import User
import datetime

class DocTime(models.Model):
    data = models.DateField
    time = models.TimeField
    doc = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doc_time", limit_choices_to={"ut": 3})
    free = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doc.name}"
    class Meta:
        verbose_name_plural = "4. Vaqt Sarhisobi"
        verbose_name = "Vaqt"


class Service(models.Model):
    name = models.CharField(max_length=512)
    info = models.TextField()
    icon = models.ImageField(upload_to="service")

    class Meta:
        verbose_name_plural = "2. Servislar"
        verbose_name = "Servis"
    def __str__(self):
        return f"{self.name}"


class Price(models.Model):
    doc = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_prices", limit_choices_to={"ut": 3})
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.CharField(max_length=123, default="50 000 uzs")
    pr = models.IntegerField(editable=False, null=True, blank=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    year = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.doc.name} {self.service.name} {self.price}"

    def save(self, *args, **kwargs):
        pr = self.price.replace(" ", "")
        for i in ["uzs", "usd", "$", "rub"]:
            pr = pr.lower().replace(i, "")
        self.pr = int(pr)
        return super(Price, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = "3. Narxlar"
        verbose_name = "Price"



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
    service = models.ForeignKey(Service,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.doc.name} -- {self.service.name}"

# class Rating(models.Model):
#     # user = models.ForeignKey(User ,on_delete=models.SET_NULL)
#     doc = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     star = models.SmallIntegerField(choices=[
#         (1, " * "),
#         (2, " ** "),
#         (3, " *** "),
#         (4, " **** "),
#         (5, " ***** "),
#     ])
#     feed = models.TextField()
