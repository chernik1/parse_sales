from django.db import models

# Create your models here.

class ParserDelete(models.Model):

    id_purchase = models.CharField(max_length=10000, default='')

    def __str__(self):
        return f'{self.id_purchase}'

class Parser(models.Model):

    id = models.CharField(max_length=100, primary_key=True)
    keyword = models.CharField(max_length=10000, default='')
    id_purchase = models.CharField(max_length=10000, default='')
    name_company = models.CharField(max_length=10000, default='')
    name_purchase = models.CharField(max_length=10000, default='')
    date = models.CharField(max_length=10000, default='')
    price = models.CharField(max_length=10000, default='')
    payer_number = models.CharField(max_length=10000, default='')

    def __str__(self):
        return f'{self.keyword} - {self.name_purchase}'


class ParserZaku(models.Model):

    keyword = models.CharField(max_length=10000, default='')
    url = models.CharField(max_length=10000, default='')
    name_company = models.CharField(max_length=10000, default='')
    name_purchase = models.CharField(max_length=10000, default='')
    main_name_purchase = models.CharField(max_length=10000, default='')
    name_purchase = models.CharField(max_length=10000, default='')
    price = models.CharField(max_length=10000, default='')

    def __str__(self):
        return f'{self.keyword} - {self.name_purchase}'