# Generated by Django 5.2.4 on 2025-07-09 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0003_menulink_site_setup'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetup',
            name='favicon',
            field=models.ImageField(blank=True, null=True, upload_to='assets/favicon/%Y/%m/', verbose_name='Favicon'),
        ),
    ]
