# Generated by Django 5.0.3 on 2024-07-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0007_remove_precard_stu_precard_pw_precard_stus'),
    ]

    operations = [
        migrations.AddField(
            model_name='precard',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]