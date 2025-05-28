from django.db import models


# Create your models here.
class Core(models.Model):

    name = models.CharField(unique=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def increase(self):
        self.value += 1
        self.save()
