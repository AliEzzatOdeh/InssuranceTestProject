# Generated by Django 2.0.2 on 2018-02-10 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20180209_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='field_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='field_type', to='api.FieldType'),
        ),
    ]
