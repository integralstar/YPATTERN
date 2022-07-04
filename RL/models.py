from django.db import models


class A3C(models.Model):
    emulator = models.BooleanField(default=False)
