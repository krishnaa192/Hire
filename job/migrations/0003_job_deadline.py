# Generated by Django 4.2.4 on 2023-09-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_job_category_remove_applicantprofile_current_ctc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
