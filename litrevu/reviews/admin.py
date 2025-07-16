from django.contrib import admin
from .models import Ticket, Review, Comment, UserFollows

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'created_at',    # ← champ renommé
    )
    list_filter = (
        'created_at',    # ← champ renommé
    )
    search_fields = (
        'title',
        'description',
        'user__username',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'headline',
        'ticket',
        'user',
        'rating',
        'time_created',
    )
    list_filter = (
        'rating',
        'time_created',
    )
    search_fields = (
        'headline',
        'body',
        'user__username',
        'ticket__title',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'user',
        'time_created',
    )
    list_filter = (
        'time_created',
    )
    search_fields = (
        'body',
        'user__username',
    )


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'followed_user',
    )
    search_fields = (
        'user__username',
        'followed_user__username',
    )
