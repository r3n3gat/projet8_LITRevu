# litrevu/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Hérite de AbstractUser pour ajouter un champ de biographie
    correspondant à ce que votre fixture JSON contient.
    """
    bio = models.TextField(
        max_length=500,
        blank=True,
        default="",
        help_text="Biographie de l’utilisateur (facultatif)"
    )

    def __str__(self):
        return self.username
