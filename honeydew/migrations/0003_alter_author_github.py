# Generated by Django 5.1.1 on 2024-11-24 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honeydew', '0002_alter_author_github_alter_author_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='github',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
