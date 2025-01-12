from django.db import models
class Car(models.Model):
    name = models.CharField('Название автомобиля', max_length=30)
# Create your models here.
