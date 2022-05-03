# Generated by Django 3.2.5 on 2022-04-07 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('fundacion', models.PositiveSmallIntegerField(default=0)),
                ('estadio', models.CharField(max_length=30)),
                ('aforo', models.PositiveIntegerField(default=0)),
                ('direccion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveSmallIntegerField()),
                ('fecha', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Temporada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anyo', models.PositiveSmallIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goles_local', models.PositiveSmallIntegerField()),
                ('goles_visitante', models.PositiveSmallIntegerField()),
                ('jornada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.jornada')),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jornada_local', to='principal.equipo')),
                ('visitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jornada_visitante', to='principal.equipo')),
            ],
        ),
        migrations.AddField(
            model_name='jornada',
            name='temporada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.temporada'),
        ),
        migrations.AlterUniqueTogether(
            name='jornada',
            unique_together={('temporada', 'numero')},
        ),
    ]
