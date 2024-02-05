from app.models.doctor import Graph
from faker import Faker
fake = Faker()


def sead_db(n):
    for i in range(0,n):
        Graph.objects.create(
            teacher_info = fake.name(),
            title = fake.title(),
            links = fake.links(),
            value = fake.value(),
            year = fake.year()
        )