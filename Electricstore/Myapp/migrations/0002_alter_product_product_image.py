# Generated by Django 3.2 on 2021-12-13 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.FileField(blank=True, upload_to='img/%m'),
        ),
    ]