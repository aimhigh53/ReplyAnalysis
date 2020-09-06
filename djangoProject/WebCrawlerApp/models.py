from django.db import models

class crawler(models.Model):
    newstitle=models.CharField(max_length=200)
    contents = models.CharField(max_length=500)
    recommand = models.IntegerField()
    unrecommand = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        db_table='crawler'

