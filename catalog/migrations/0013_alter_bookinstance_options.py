# Generated by Django 4.1.4 on 2023-01-01 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['status', 'loaned_on', 'due_back']},
        ),
    ]