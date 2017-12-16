from django.db import models

# Create your models here.
class Address(models.Model):
	name = models.CharField(max_length= 100, blank=True, null=True)
	street = models.CharField(max_length= 100, blank=True, null=True)
	housenumber = models.CharField(max_length= 10, blank=True, null=True)
	postcode = models.IntegerField(blank=True, null=True)
	city = models.CharField(max_length= 50, blank=True, null=True)
	country = models.CharField(max_length= 20, blank=True, null=True, default= "Slovakia")
	latitude= models.DecimalField(max_digits=20, decimal_places=18, default=48.721287)
	longitude = models.DecimalField(max_digits=20, decimal_places=18, default= 18.5491726)

	def __str__(self):
		return u'[{}]_{}' .format(self.city, self.name)

	@models.permalink
	def get_absolute_url(self):
		return ('address-detail', [self.id])

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Address._meta.fields]


class Tour(models.Model):
	date = models.DateField()
	stops = models.ManyToManyField(Address)
	start_location = models.ForeignKey(Address, related_name='start_address', on_delete=models.CASCADE)
	end_location = models.ForeignKey(Address, related_name='end_address', on_delete=models.CASCADE)
	drivers = models.IntegerField(default=3)
	notes = models.TextField(null=True, blank= True)

	def __str__(self):
		return u'Tour of {}' .format(self.date)


class Vehicle(models.Model):
	name = models.CharField(max_length= 100)
	capacity = models.IntegerField(default=7)
	comment = models.TextField(null=True, blank= True)

	def __str__(self):
		return u'{}_[capacity {}]' .format(self.name, self.capacity)

