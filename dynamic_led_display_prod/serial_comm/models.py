from django.db import models

# Create your models here.

class SerialCommunication(models.Model):
    RTC = models.DateTimeField()
    WSPD = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    WDIR = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    ATMP = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    HUMD = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    RAIN = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    SRAD = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    BPRS = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    WDCH = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    DWPT = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    P12 = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    P13 = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    P14 = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    P15 = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)
    P16 = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=10)

    def __str__(self) -> str:
        return_str = f"{self.RTC} => {self.WSPD} | {self.WDIR} | {self.ATMP} | {self.HUMD} | {self.RAIN} | {self.SRAD} | {self.BPRS} | {self.WDCH} | {self.DWPT} | {self.P12} | {self.P13} | {self.P14} | {self.P15} | {self.P16}"
        return return_str