# Generated by Django 3.0.4 on 2020-03-20 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20200309_1833'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created_dt']},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-last_message__created_dt', '-created_dt']},
        ),
        migrations.AddField(
            model_name='room',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
