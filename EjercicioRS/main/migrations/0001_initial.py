# Generated by Django 3.2.5 on 2022-05-12 10:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('idCategoria', models.TextField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(verbose_name='Categoría')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Ocupacion',
            fields=[
                ('ocupacionId', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True, verbose_name='Ocupación')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('idPelicula', models.TextField(primary_key=True, serialize=False)),
                ('titulo', models.TextField(verbose_name='Título')),
                ('fechaEstreno', models.DateField(null=True, verbose_name='Fecha de Estreno')),
                ('imdbUrl', models.URLField(verbose_name='URL en IMDB')),
                ('categorias', models.ManyToManyField(to='main.Categoria')),
            ],
            options={
                'ordering': ('titulo', 'fechaEstreno'),
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('idUsuario', models.TextField(primary_key=True, serialize=False)),
                ('edad', models.IntegerField(help_text='Debe introducir una edad', verbose_name='Edad')),
                ('sexo', models.CharField(help_text='Debe elegir entre M o F', max_length=1, verbose_name='Sexo')),
                ('codigoPostal', models.TextField(verbose_name='Código Postal')),
                ('ocupacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.ocupacion')),
            ],
            options={
                'ordering': ('idUsuario',),
            },
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField(choices=[(1, 'Muy mala'), (2, 'Mala'), (3, 'Regular'), (4, 'Buena'), (5, 'Muy Buena')], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Puntuación')),
                ('idPelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pelicula')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.usuario')),
            ],
            options={
                'ordering': ('idPelicula', 'idUsuario'),
            },
        ),
        migrations.AddField(
            model_name='pelicula',
            name='puntuaciones',
            field=models.ManyToManyField(through='main.Puntuacion', to='main.Usuario'),
        ),
    ]
