# litrevu/reviews/models.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Ticket(models.Model):
    title = models.CharField(
        max_length=128,
        help_text="Titre du livre ou de l’article à critiquer"
    )
    description = models.TextField(
        max_length=2048,
        blank=True,
        help_text="Description ou contexte (facultatif)"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    cover_image = models.ImageField(
        upload_to='ticket_images/',
        null=True,
        blank=True,
        help_text="Couverture (facultative)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de création"
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} demandé par {self.user.username}"


class Review(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Note de 0 à 5 étoiles"
    )
    headline = models.CharField(
        max_length=128,
        help_text="Titre de votre critique"
    )
    body = models.TextField(
        max_length=8192,
        blank=True,
        help_text="Texte de la critique (facultatif)"
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de création"
    )

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return f"{self.headline} ({self.rating}★)"


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField(
        max_length=2048,
        help_text="Texte du commentaire"
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de création"
    )

    class Meta:
        ordering = ['time_created']

    def __str__(self):
        return f"Commentaire de {self.user.username} sur {self.review.headline}"


class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    class Meta:
        unique_together = ('user', 'followed_user')

    def clean(self):
        if self.user == self.followed_user:
            raise ValidationError("Vous ne pouvez pas vous suivre vous-même.")

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"
