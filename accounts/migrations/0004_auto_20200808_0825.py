# Generated by Django 3.0.8 on 2020-08-08 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_post_recipient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.FileField(null=True, upload_to='upload/'),
        ),
    ]
