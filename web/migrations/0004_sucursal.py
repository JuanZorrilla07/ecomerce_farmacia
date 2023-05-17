# Generated by Django 3.2 on 2023-05-17 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_pedido_pedidodetalle'),
    ]

    operations = [
        migrations.CreateModel(
            name='sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dirrecion', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=8)),
                ('nombre', models.CharField(choices=[('Cerro', 'Cerro'), ('Sayago', 'Sayago'), ('Malvin', 'Malvin'), ('Centro', 'Centro')], default='Centro', max_length=6)),
                ('imagen', models.ImageField(blank=True, upload_to='productos')),
                ('link', models.CharField(blank=True, max_length=300)),
                ('horario', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
