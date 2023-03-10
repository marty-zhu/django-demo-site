# Generated by Django 4.1.4 on 2023-01-25 17:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_alter_bookinstance_imprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.IntegerField(editable=False, help_text='The ISBN number of the book', primary_key=True, serialize=False, unique=True, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='copy_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text="The ID of the book in the catalog's stock", primary_key=True, serialize=False),
        ),
    ]
