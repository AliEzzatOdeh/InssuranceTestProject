# Generated by Django 2.0.2 on 2018-02-09 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20180209_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtypeenumvalues',
            name='field_associated_with_enum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enum_values', to='api.Field'),
        ),
    ]
