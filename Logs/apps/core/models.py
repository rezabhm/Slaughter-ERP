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


class ViewsRoles(models.Model):

    view_name = models.CharField(max_length=50)
    method = models.CharField(default='GET', choices=(
                    ('GET', 'GET'),
                    ('POST', 'POST'),
                    ('DELETE', 'DELETE'),
                    ('PATCH', 'PATCH'),
                    ('PUT', 'PUT'),
                )
    )
    roles = models.JSONField()

    def __str__(self):
        return f'{self.view_name}__{self.method}'
