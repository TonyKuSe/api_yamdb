# Generated by Django 3.2 on 2023-10-01 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_emailverification_confirm_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverification',
            name='confirm_code',
            field=models.CharField(default=123456, max_length=6),
            preserve_default=False,
        ),
    ]