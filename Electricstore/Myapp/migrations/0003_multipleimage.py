# Generated by Django 3.2 on 2021-12-13 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0002_alter_product_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Multipleimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(upload_to='img/%m')),
                ('prod', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Myapp.product')),
            ],
        ),
    ]