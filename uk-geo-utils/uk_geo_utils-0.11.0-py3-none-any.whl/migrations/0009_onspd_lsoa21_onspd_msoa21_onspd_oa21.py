# Generated by Django 4.1.3 on 2022-11-01 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("uk_geo_utils", "0008_address_addressbase_postal"),
    ]

    operations = [
        migrations.AddField(
            model_name="onspd",
            name="lsoa21",
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AddField(
            model_name="onspd",
            name="msoa21",
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AddField(
            model_name="onspd",
            name="oa21",
            field=models.CharField(max_length=9, null=True),
        ),
    ]
