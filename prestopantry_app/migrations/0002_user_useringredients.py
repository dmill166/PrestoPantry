# Generated by Django 4.0.2 on 2022-02-21 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prestopantry_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=50)),
                ('password_hash', models.CharField(max_length=256)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('current_ind', models.BooleanField()),
                ('created_record', models.DateTimeField()),
                ('modified_record', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_id', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('current_ind', models.BooleanField()),
                ('created_record', models.DateTimeField()),
                ('modified_record', models.DateTimeField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prestopantry_app.user')),
            ],
        ),
    ]
