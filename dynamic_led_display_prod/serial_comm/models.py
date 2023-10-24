from django.db import models

# Create your models here.

class RS232(models.Model):
    RTC = models.CharField(max_length=255)
    AvgeSpeed = models.CharField(max_length=255)
    AvgeTemp = models.CharField(max_length=255)
    AvgeHum = models.CharField(max_length=255)
    AvgeSr = models.CharField(max_length=255)

    def __str__(self):        
        return f"{self.RTC} | {self.AvgeSpeed} | {self.AvgeTemp} | {self.AvgeHum} | {self.AvgeSr}"

class RS485(models.Model):
    RTC = models.CharField(max_length=255)
    AvgeSpeed = models.CharField(max_length=255)
    AvgeTemp = models.CharField(max_length=255)
    AvgeHum = models.CharField(max_length=255)
    AvgeSr = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.RTC} | {self.AvgeSpeed} | {self.AvgeTemp} | {self.AvgeHum} | {self.AvgeSr}"