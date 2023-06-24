from django.db.models.signals import post_save
from .models import UserProfile, CustomUser
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(
            user=instance,
            username=instance.username,
        )
        if instance.first_name: profile.first_name = instance.first_name
        if instance.last_name: profile.last_name = instance.last_name
        profile.save()


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created == False:
            profile = UserProfile.objects.filter(user=instance).first()
            profile.first_name = instance.first_name
            profile.last_name = instance.last_name
            profile.last_name = instance.last_name
            profile.username = instance.username
            profile.save()
    except Exception as e:
            pass