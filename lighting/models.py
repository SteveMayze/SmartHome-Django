from django.db import models
from i2c import models as i2c
from django.template.defaultfilters import slugify
from channels.binding.websockets import WebsocketBinding


# Create your models here.

class Zone( models.Model ):
    name = models.CharField(max_length=50, unique=True)
    device = models.ForeignKey( i2c.Device )
    pir_enabled = models.BooleanField(default=False)
    test_active = models.BooleanField(default=False)
    on_delay = models.IntegerField(default=10)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.device.name + ' ' + self.name)
        super(Zone, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}: {1}".format(str(self.device.name), str(self.name))

    
class LightHistory( models.Model ):
    timestamp = models.DateTimeField(unique=True)
    status = models.IntegerField()
    config = models.IntegerField()

    def __str__(self):
        return "{0}: {1}, {2}".format(str(self.timestamp), str(self.status), str(self.config))


class LightHistoryBinding(WebsocketBinding):
    model = LightHistory
    stream = "tl2c_state"
    fields = ["timestamp", "status", "config"]

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["binding.tl2c",]

    def has_permission(self, user, action, pk):
        return True

 
