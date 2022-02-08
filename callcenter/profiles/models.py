from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    snils = models.TextField(max_length=11, blank=True)
    medpolis = models.CharField(max_length=16, blank=True)
    email_confirmed = models.BooleanField(default=False)
    mobile = models.CharField(max_length=12, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
