from django.db import models


class Crawler(models.Model):
    url_address = models.ForeignKey('checker.URL', on_delete=models.CASCADE)
