# Generated by Django 4.1.4 on 2023-02-01 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_alter_book_isbn_alter_bookinstance_copy_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['status', 'loaned_on', 'due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]