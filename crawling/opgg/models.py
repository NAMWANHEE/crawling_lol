from django.db import models

class Lol(models.Model):
    rank = models.IntegerField()
    tier = models.CharField(max_length=50)
    points = models.IntegerField()
    win = models.CharField(max_length=50)
    lose = models.CharField(max_length=50)
    win_ratio = models.CharField(max_length=50)
    most1 = models.CharField(max_length=50)
    most2 = models.CharField(max_length=50)
    most3 = models.CharField(max_length=50)
    cha_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cha_name
# Create your models here.
