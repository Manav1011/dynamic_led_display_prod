from django.db import models

# Create your models here.

class Elements(models.Model):
    element_name = models.CharField(max_length=255)
    code = models.TextField()
    
    def __str__(self) -> str:
        return self.element_name

class Programs(models.Model):
    program_name = models.CharField(unique=True,max_length=255)
    elements = models.ManyToManyField(Elements,blank=True,null=True)

    def __str__(self) -> str:
        return self.program_name
