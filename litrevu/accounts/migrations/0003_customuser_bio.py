# Generated by Django 5.2.2 on 2025-07-03 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customuser_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, default='', help_text='Biographie de l’utilisateur (facultatif)', max_length=500),
        ),
    ]
