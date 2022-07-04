from django.db import models
from . import generator


class GA(models.Model):
    genome = models.TextField(max_length=generator.GENETIC_CODE_LENGTH)
    generation = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)
