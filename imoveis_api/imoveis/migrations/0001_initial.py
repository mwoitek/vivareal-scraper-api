# Generated by Django 3.1.7 on 2021-02-25 01:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=70, verbose_name='cidade')),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigla', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adicionado', models.DateTimeField(default=django.utils.timezone.now, verbose_name='adicionado em')),
                ('logradouro', models.CharField(blank=True, max_length=200)),
                ('numero', models.IntegerField(null=True, verbose_name='número')),
                ('bairro', models.CharField(max_length=70)),
                ('area', models.IntegerField(verbose_name='área (m²)')),
                ('quartos', models.IntegerField()),
                ('banheiros', models.IntegerField()),
                ('vagas', models.IntegerField()),
                ('preco', models.IntegerField(verbose_name='preço (R$)')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imoveis.cidade')),
            ],
        ),
        migrations.AddField(
            model_name='cidade',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imoveis.estado'),
        ),
    ]
