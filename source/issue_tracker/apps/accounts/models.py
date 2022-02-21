from django.contrib.auth import get_user_model
from django.db import models



class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', verbose_name='Профиль', on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/', null=False, blank=True)
    about = models.TextField(max_length=2000, null=True, blank=True, verbose_name="О себе",)
    github = models.CharField(max_length=50, null=True, blank=True, verbose_name='Ссылка на гит')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        db_table = 'profile_user'

    def __str__(self):
        return f'Профиль: {self.user.username}, {self.id}'