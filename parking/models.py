# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Spot(models.Model):
    latitude = models.FloatField()  # Lat field
    longitude = models.FloatField() # Long field
    available = models.BooleanField(default=True)  # Check to see if spot is available
    parkingStartTime = models.DateTimeField(null=True)  # Starttime of a reserved space
    parkingAllocatedTime = models.FloatField(null=True) # Allocated time in minutes for a reserved space

    def __str__(self):
        return "<%s, lat: %s, long: %s, available: %s>" % (self.id, 
                                                           self.latitude, 
                                                           self.longitude, 
                                                           self.available)


