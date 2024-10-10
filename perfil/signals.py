from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import Perfil
from blog.models import Post
import os

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        perfil = Perfil.objects.create(usuario=instance)
        perfil.save()
    else:
        ...
        # Atualizando o Perfil


# Sinal Blog - Início
def delete_image(instance):
		try:
			os.remove(instance.foto.path)
		except (ValueError, FileNotFoundError):
			...

@receiver(pre_save, sender=Post)
def delete_image_updated(sender, instance, *args, **kwargs):
    if instance.id:
        old_instance = Post.objects.get(id=instance.id)
        # print('Trocou a imagem?', old_instance.foto != instance.foto)
        if old_instance.foto != instance.foto:
            delete_image(old_instance)
    

@receiver(pre_delete, sender=Post)
def delete_image_pre_delete(sender, instance, *args, **kwargs):
    old_instance = Post.objects.get(id=instance.id)
    delete_image(old_instance)
# Sinal Blog - Fim