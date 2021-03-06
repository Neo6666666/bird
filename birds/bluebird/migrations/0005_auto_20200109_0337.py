# Generated by Django 3.0.2 on 2020-01-09 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0004_auto_20200104_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Normative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('since_date', models.DateField(blank=True, null=True)),
                ('up_to_date', models.DateField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NormativeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('normative', models.ManyToManyField(related_name='normatives', to='bluebird.Normative')),
            ],
        ),
        migrations.AlterField(
            model_name='contragent',
            name='norm_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bluebird.NormativeCategory'),
        ),
    ]
