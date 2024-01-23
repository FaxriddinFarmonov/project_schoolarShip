from app.models.books import Books
import random
from django.db import  connection



def hello():
    number = random.randint(2, 1000)
    book = Books.objects.create(
        number=number
    )
    book.save()


