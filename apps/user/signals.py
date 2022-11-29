from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.user.base_category import base_categories
from .models import UserProfile, Transaction
from .utils import create_base_categories


@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs) -> None:
    """
    Создает для нового пользователя профиль и задает ему стандартные категории

    :param sender: User модель
    :param instance: User
    :param created: Создался ли он
    """

    if created:
        create_base_categories(base_categories, instance)

        UserProfile.objects.create(user=instance, balance=0)


@receiver(post_save, sender=Transaction)
def transaction_created_handler(sender, instance, created, **kwargs) -> None:
    if created:
        user_pofile: UserProfile = UserProfile.objects.get(user=instance.user)
        if instance.sum is not None:
            if instance.type == 'top up':
                user_pofile.balance += instance.sum
            else:
                user_pofile.balance -= instance.sum
        user_pofile.save()
