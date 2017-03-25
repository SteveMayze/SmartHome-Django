from django.db import models
from django.template.defaultfilters import slugify
from django_pandas.managers import DataFrameManager

class Resource( models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Resource, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class ResourceValueFactor( models.Model ):
    resource = models.ForeignKey( Resource )
    start_year = models.IntegerField( blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    billing_factor = models.DecimalField(max_digits=9, decimal_places=4)
    status_value = models.DecimalField(max_digits=9, decimal_places=4)
    factor = models.DecimalField(max_digits=9, decimal_places=4)

    def __str__(self):
        return "{0} - {1} - {2}: {3}".format(str(self.resource.name), str(self.start_year),
                                       str(self.end_year), str(self.factor))
 

class ResourceEntry( models.Model ):
    resource = models.ForeignKey( Resource )
    time_stamp = models.DateField()
    value_open = models.DecimalField( max_digits=9, decimal_places=4)
    value_close = models.DecimalField( max_digits=9, decimal_places=4)
    # Adjustments are made when there is a meter change, for instance.
    value_adjust = models.DecimalField( max_digits=9, decimal_places=4)
    value_usage = models.DecimalField( max_digits=9, decimal_places=4)
    comment = models.CharField(max_length=200, blank=True, null=True)

    objects = DataFrameManager()


    class Meta:
        verbose_name_plural = 'ResourceEntries'

    def __str__(self):
        return "{0} - {1}: {2}".format(str(self.resource.name),
                                       str(self.time_stamp),
                                       str(self.value_usage))
