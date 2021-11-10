from django.db import models
from django.contrib.auth.models import User

class trip_details(models.Model):
    user = models.ForeignKey("taxiairnl.user_details",on_delete=models.SET_NULL,blank=True,null=True)
    from_loc = models.CharField(max_length=500,blank=True,null=True)
    to_loc = models.CharField(max_length=500,blank=True,null=True)
    date_time = models.DateTimeField(blank=True,null=True)
    vehicle = models.CharField(max_length=100,blank=True,null=True)
    price = models.CharField(max_length=100,blank=True,null=True)
    is_paid = models.BooleanField(default=False)
    is_local = models.BooleanField(default=False)
    dist = models.CharField(max_length=100,blank=True,null=True)
    timet = models.CharField(max_length=100,blank=True,null=True)
    objnum = models.CharField(max_length=100,blank=True,null=True)
    remarks = models.CharField(max_length=1000,blank=True,null=True)
    is_return = models.BooleanField(default=False)
    is_babystoel = models.BooleanField(default=False)
    flight_number = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        try:
            return "{}-{}".format(self.id,self.user.username)
        except:
            return "{}-".format(self.id)

class user_details(models.Model):
    username = models.CharField(max_length=400,blank=True,null=True)
    email = models.CharField(max_length=400,blank=True,null=True)
    number = models.CharField(max_length=400,blank=True,null=True)

    def __str__(self):
        try:
            return "{}-{}".format(self.id,self.username)
        except:
            return "{}-".format(self.id)


class registered_riders(models.Model):
    full_name = models.CharField(max_length=500,null=True,blank=True)
    email = models.CharField(max_length=500,null=True,blank=True)
    phone_number = models.CharField(max_length=500,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)

    def __str__(self):
        try:
            return "{}-{}".format(self.id,self.full_name)
        except:
            return "{}-".format(self.id)