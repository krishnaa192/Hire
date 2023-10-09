# Generated by Django 4.2.4 on 2023-09-24 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_alter_education_degree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='degree',
            field=models.CharField(choices=[('B.Tech', 'B.Tech'), ('B.E', 'B.E'), ('B.Sc', 'B.Sc'), ('B.Com', 'B.Com'), ('B.A', 'B.A'), ('M.Tech', 'M.Tech'), ('M.E', 'M.E'), ('M.Sc', 'M.Sc'), ('M.Com', 'M.Com'), ('M.A', 'M.A'), ('Phd', 'Phd'), ('Diploma', 'Diploma'), ('HighSchool', 'HighSchool'), ('Intermediate', 'Intermediate')], max_length=100),
        ),
    ]
