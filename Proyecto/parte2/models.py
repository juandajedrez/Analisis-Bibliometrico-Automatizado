from django.db import models


class ResulAlgorithm(models.Model):
    keyArticleOne = models.CharField(max_length=20)
    keyArticleTwo = models.CharField(max_length=20)
    result = models.IntegerField()

    def __str__(self):
        return f"{self.keyArticleOne} - {self.keyArticleTwo}: {self.result}"
