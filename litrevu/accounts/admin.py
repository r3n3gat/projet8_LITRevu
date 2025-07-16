from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Personnalisation de l'affichage et des champs du CustomUser
    dans l'interface d'administration Django.
    """
    # On ajoute le champ 'bio' aux fieldsets existants de UserAdmin
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('bio',),
        }),
    )
    # Colonnes affichées dans la liste des utilisateurs
    list_display = ('username', 'email', 'is_staff', 'is_active')
    # Filtres proposés dans la barre latérale
    list_filter = ('is_staff', 'is_active')
