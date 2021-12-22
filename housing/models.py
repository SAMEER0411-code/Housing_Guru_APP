from django.db import models

# Create your models here.
class user(models.Model):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    passwd = models.CharField(max_length=40)
    phone= models.IntegerField()
    gender=models.CharField(max_length=6)

    def __str__(self):
        return f"{self.email}"


class postmodel(models.Model):
    description = models.CharField(max_length=100)
    area= models.CharField(max_length=100)
    zipcode =models.IntegerField()
    rent=models.IntegerField()
    facilities=models.CharField(max_length=100)
    meals=models.CharField(max_length=100)
    name=models.EmailField()
    contact=models.IntegerField()
    roompic =models.ImageField()


    def __str__(self):
        return "{}".format(self.name)