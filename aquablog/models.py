from django.db import models
from django.contrib.auth.models import User
from zinnia.models import *

class UserProfile(models.Model):
    avatar = models.ImageField("Profile Pic", upload_to="images/", blank=True, null=True)
    posts = models.IntegerField(default=0)
    user = models.ForeignKey(User, unique=True)
    categories = models.ManyToManyField(Category)
    #control_print = "Bla bla bla"
    #docfile = models.FileField(upload_to='images')

    def __unicode__(self):
        return unicode(self.user)

class Document(models.Model):
    docfile = models.FileField(upload_to='images')