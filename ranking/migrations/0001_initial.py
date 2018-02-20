# Generated by Django 2.0.2 on 2018-02-19 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('match_date', models.DateField()),
                ('begins', models.TimeField(blank=True, null=True)),
                ('ends', models.TimeField(blank=True, null=True)),
                ('medal_limit', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Matches',
                'ordering': ['-match_date'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Verein',
                'verbose_name_plural': 'Vereine',
            },
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='participations', to='ranking.Match')),
            ],
            options={
                'verbose_name': 'Teilnahme',
                'verbose_name_plural': 'Teilnahmen',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='results', to='ranking.Match')),
            ],
            options={
                'verbose_name': 'Resultat',
                'verbose_name_plural': 'Resultate',
            },
        ),
        migrations.CreateModel(
            name='Shooter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('family_name', models.CharField(max_length=128)),
                ('date_of_birth', models.DateField()),
                ('license_number', models.CharField(max_length=32, null=True)),
                ('is_supervisor', models.BooleanField(default=False, verbose_name='Schützenmeister')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='members', to='ranking.Organization')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shooter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Schütze',
                'verbose_name_plural': 'Schützen',
            },
        ),
        migrations.AddField(
            model_name='result',
            name='shooter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='shooters', to='ranking.Shooter'),
        ),
        migrations.AddField(
            model_name='participation',
            name='shooter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='participations', to='ranking.Shooter'),
        ),
        migrations.AddField(
            model_name='match',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ranking.Organization'),
        ),
        migrations.AddField(
            model_name='match',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ranking.Shooter', verbose_name='Schützenmeister'),
        ),
    ]
