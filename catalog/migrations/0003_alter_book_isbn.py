# Generated by Django 4.1.4 on 2022-12-28 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_rename_authors_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.IntegerField(help_text='The ISBN number of the book', max_length=13, primary_key=True, serialize=False, unique=True, verbose_name='ISBN'),
        ),
    ]