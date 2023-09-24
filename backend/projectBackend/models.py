from django.db import models


class Tech(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    tech = models.CharField(max_length=256)

    def __str__(self):
        return self.title
