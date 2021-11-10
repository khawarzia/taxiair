from django.db import models

class variable_pricings(models.Model):
    minimum_price = models.FloatField(default=0)
    km_price = models.FloatField(default=0)
    minute_price = models.FloatField(default=0)
    from_person = models.IntegerField(default=0)
    to_person = models.IntegerField(default=0)
    vehicle_type = models.CharField(max_length=200)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.vehicle_type

class fixed_pricings(models.Model):
    airport_name = models.CharField(max_length=200)
    to_or_from = models.CharField(max_length=200)
    sedan_price = models.FloatField(default=0)
    bus_price = models.FloatField(default=0)
    xxl_bus_price = models.FloatField(default=0)
    
    def __str__(self):
        return "{} <-> {}".format(self.airport_name,self.to_or_from)