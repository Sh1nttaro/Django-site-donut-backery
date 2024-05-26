from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# Создаем и сохраняем профиль пользователя при создании или обновлении пользователя
@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        # Если пользователь создан, создаем профиль
        Profile.objects.create(user=instance)
    # Всегда сохраняем профиль пользователя при сохранении пользователя
    instance.profile.save()