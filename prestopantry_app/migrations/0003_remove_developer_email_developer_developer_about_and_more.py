# Generated by Django 4.0.1 on 2022-04-01 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestopantry_app', '0002_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer',
            name='email',
        ),
        migrations.AddField(
            model_name='developer',
            name='developer_about',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='developer',
            name='git_hub_link',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='developer',
            name='linkedin_link',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='developer',
            name='first_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='developer',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]