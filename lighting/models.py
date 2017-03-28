from django.db import models
from i2c import models as i2c

# Create your models here.

class Zone( models.Model ):
    name = models.CharField(max_length=50, unique=True)
    device = models.ForeignKey( i2c.Device )
    pir_enabled = models.BooleanField(default=False)
    test_active = models.BooleanField(default=False)
    on_delay = models.IntegerField(default=10)

    def __str__(self):
        return "{0}: {1}".format(str(self.device.name), str(self.name))

    
