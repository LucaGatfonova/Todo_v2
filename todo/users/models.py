from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(AbstractUser):
    def __str__(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username

    class Meta(object):
        unique_together = ('email',)    # делает уникальным
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


@receiver(pre_save, sender=User)
def user_pre_save(sender, **kwargs):
    email = kwargs['instance'].email
    username = kwargs['instance'].username

    if not email:
        raise ValidationError("email required")

    if sender.objects.filter(email=email).exclude(username=username).count():
        raise ValidationError("email needs to be unique")


