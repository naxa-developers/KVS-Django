from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import os.path


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
    image_thumbnail = models.ImageField(upload_to='thumbs', editable=False, null=True, blank=True)


    def make_thumbnail(self):

        image = Image.open(self.image)
        image.thumbnail((600, 400), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.image_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


    def save(self, *args, **kwargs):

        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(AboutProject, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class OverallSystemFeatures(models.Model):
    heading = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='image')
    title = models.CharField(max_length=500)
    feature1 = models.CharField(max_length=500, blank=True, null=True)
    feature2 = models.CharField(max_length=500, blank=True, null=True)
    feature3 = models.CharField(max_length=500, blank=True, null=True)
    feature4 = models.CharField(max_length=500, blank=True, null=True)
    feature5 = models.CharField(max_length=500, blank=True, null=True)
    feature6 = models.CharField(max_length=500, blank=True, null=True)
    feature7 = models.CharField(max_length=500, blank=True, null=True)
    feature8 = models.CharField(max_length=500, blank=True, null=True)
    image_thumbnail = models.ImageField(upload_to='thumbs', editable=False, null=True, blank=True)


    def make_thumbnail(self):

        image = Image.open(self.image)
        image.thumbnail((600, 400), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.image_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


    def save(self, *args, **kwargs):

        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(OverallSystemFeatures, self).save(*args, **kwargs)

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