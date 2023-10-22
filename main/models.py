from django.db import models

# Create your models here.

class Parser(models.Model):

    keyword = models.CharField(max_length=10000)
    name_company = models.CharField(max_length=10000)
    name_purchase = models.CharField(max_length=10000)
    date = models.CharField(max_length=10000)
    price = models.CharField(max_length=10000)

    def __str__(self):
        return f'{self.keyword} - {self.name_purchase}'


