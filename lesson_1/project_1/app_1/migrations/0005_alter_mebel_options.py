# Generated by Django 5.1.4 on 2025-01-18 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0004_alter_mebel_options_mebel_pars_datetime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mebel',
            options={'ordering': ['pars_datetime', '-price'], 'verbose_name': 'Мебель', 'verbose_name_plural': 'Мебель'},
        ),
    ]