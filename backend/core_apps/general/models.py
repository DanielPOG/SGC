from django.db import models

# Create your models here.
class Regional(models.Model):
    codigoRegional= models.CharField(max_length=10, unique=True)
    nombre= models.CharField(max_length=100, unique=True)
class Centro(models.Model):
    codigoCentro= models.CharField(max_length=10, unique=True)
    nombre= models.CharField(max_length=100, unique=True)
    regional= models.ForeignKey('Regional', on_delete=models.CASCADE)
class Red(models.Model):
    codigoRed= models.CharField(max_length=10, unique=True)
    nombre= models.CharField(max_length=100, unique=True)
    centro= models.ForeignKey('Centro', on_delete=models.CASCADE)
class Area(models.Model):
    codigoArea= models.CharField(max_length=10, unique=True)
    nombre= models.CharField(max_length=100, unique=True)
    red= models.ForeignKey('Red', on_delete=models.CASCADE)

class Dependencia(models.Model):
    codigoDependencia= models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100, unique= True)