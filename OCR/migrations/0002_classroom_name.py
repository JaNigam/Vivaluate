# Generated by Django 4.0.3 on 2022-03-10 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OCR', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
