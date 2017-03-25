from django.db import models
from django.template.defaultfilters import slugify


class Device( models.Model ):
     address = models.IntegerField()
     name = models.CharField(max_length=60)
     description = models.CharField(max_length=200)
     slug = models.SlugField()

     def save(self, *args, **kwargs):
          self.slug = slugify(str(self.address))
          super(Device, self).save(*args, **kwargs)

     def __str__(self):
          return str(self.address) + " " + self.description

    
    
