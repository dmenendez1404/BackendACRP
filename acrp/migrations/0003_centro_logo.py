# Generated by Django 2.1.5 on 2019-01-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acrp', '0002_auto_20190115_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='centro',
            name='logo',
            field=models.ImageField(null=True, upload_to='centros/'),
        ),
    ]
