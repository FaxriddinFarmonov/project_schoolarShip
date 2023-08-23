from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager


class Professions(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name_plural = "5. Kasblar"
        verbose_name = "Kasb"


class Position(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name_plural = "6. lavozim"
        verbose_name = "Lavozim"


class CstManager(UserManager):
    def create_user(self, phone=None, email=None, password=None, **extra_fields):
        if "is_staff" not in extra_fields.keys() or "is_superuser" not in extra_fields.keys():
            extra_fields.setdefault("is_staff", False)
            extra_fields.setdefault("is_superuser", False)

        user = self.model(
            phone=phone,
            email=email,
            password=password,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField("ismi", max_length=128)
    familya = models.CharField("familya", max_length=128)
    phone = models.CharField("Telefon raqami", max_length=20, unique=True)
    img = models.ImageField("rasm", upload_to="docs", null=True)
    prof = models.ForeignKey(Professions, verbose_name="SHifokor Mutaxasisligi", on_delete=models.SET_NULL, null=True)
    prosition = models.ForeignKey(Position, verbose_name="SHifokor lavozimi", on_delete=models.SET_NULL, null=True)
    info = models.TextField("SHifokor haqida qisqacha", null=True)
    email = models.EmailField("Elektron pochtasi", null=True)
    gender = models.BooleanField("JInsi", default=True)

    ut = models.SmallIntegerField("Foydalanuvchi statusi", choices=[
        (1, "Boshliq"),
        (2, "Admin"),
        (3, "Doktor"),
        (4, "Mijozlar"),
    ], default=4)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CstManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELD = ['phone', "ut"]
    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name_plural = "1. Duxtirlar"
        verbose_name = "Duxtirlar"

    def save(self, *args, **kwargs):
        if self.ut == 4:
            self.position = 2
        return super(User,self).save(*args,**kwargs)