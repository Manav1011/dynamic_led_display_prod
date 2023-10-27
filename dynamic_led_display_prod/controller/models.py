from django.db import models
from django.db.models import F, Case, When
import json

# Create your models here.

class Elements(models.Model):
    element_name = models.CharField(max_length=255)
    code = models.TextField()
    
    def __str__(self) -> str:
        return self.element_name

class Programs(models.Model):
    program_name = models.CharField(unique=True,max_length=255)
    elements = models.ManyToManyField(Elements,blank=True,null=True)
    code = models.TextField(blank=True,null=True)
    running_time = models.PositiveIntegerField(default=1)
    panel_code = models.TextField(blank=True,null=True)

    def __str__(self) -> str:
        return self.program_name
    

class Panel(models.Model):
    programs = models.ManyToManyField(Programs,blank=True,null=True)
    styles = models.TextField(blank=True,null=True)
    sequence = models.JSONField(max_length=256,blank=True,null=True) 
    channel_name = models.CharField(max_length=255,blank=True,null=True)

    def return_program_in_order(self):
        if self.sequence:
            custom_order_json = json.loads(self.sequence)            
            custom_order = custom_order_json['program_sequence']
            # Build a list of When whens = [When(id=id, then=index) for index, id in enumerate(custom_order)]expressions for each ID
            
            whens = [When(id=id, then=index) for index, id in enumerate(custom_order)]
            # Create a Case expression that assigns a custom order based on the specified IDs
            custom_order_expression = Case(*whens, default=F('id'), output_field=models.IntegerField())

            # Retrieve the related programs in the custom order
            programs_in_custom_order = self.programs.all().order_by(custom_order_expression)
            return programs_in_custom_order
        else:
            return self.programs.all()
