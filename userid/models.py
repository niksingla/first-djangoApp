
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ImageField
from django_countries.fields import CountryField


    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = CountryField(blank_label='--')
    profile_pic = models.ImageField(default="default.jpg", upload_to="images/")
    
    def __str__(self):
        return self.user.username


"""@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.UserProfile.save()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    instance.UserProfile.update()"""