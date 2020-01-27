from django.db import models

# Create your models here.

class Header(models.Model):
    image = models.ImageField(upload_to='image')
    title = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='image')

    def __str__(self):
        return self.title


class AboutProject(models.Model):
    heading = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='image')
    title = models.CharField(max_length=500)
    description = models.TextField()

    def __str__(self):
        return self.title


class OverallSystemFeatures(models.Model):
    heading = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='image')
    title = models.CharField(max_length=500)
    feature1 = models.CharField(max_length=500)
    feature2 = models.CharField(max_length=500)
    feature3 = models.CharField(max_length=500)
    feature4 = models.CharField(max_length=500)
    feature5 = models.CharField(max_length=500)
    feature6 = models.CharField(max_length=500)
    feature7 = models.CharField(max_length=500)
    feature8 = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class OurMission(models.Model):
    description = models.TextField()
    logo1 = models.ImageField(upload_to='image')
    logo2 = models.ImageField(upload_to='image')
    logo3 = models.ImageField(upload_to='image')


class Contact(models.Model):
    location = models.CharField(max_length=500)
    location_icon = models.ImageField(upload_to='icon')
    number = models.CharField(max_length=500)
    number_icon = models.CharField(max_length=500)
    email = models.EmailField()
    email_icon = models.EmailField()
    footer_txt = models.CharField(max_length=100)