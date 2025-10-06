from django.db import models


class ResulAlgorithm(models.Model):
    keyArticleOne = models.CharField(max_length=20)
    keyArticleTwo = models.CharField(max_length=20)
    result = models.IntegerField(max_length=20)


# Create your models here.
